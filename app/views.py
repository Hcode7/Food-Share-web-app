from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Food, Recipe, FeedBack, Subscription, Category, Cuisine
from .forms import FoodForm, RecipeForm, FeedBackForm
from time import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from account.models import Profile
from django.db.models import Count

# Create your views here.

def home(request):
    search = request.GET.get('search')
    if search:
        foods = Food.objects.filter(title__icontains=search)

        context = {
            'foods' : foods,
            'search' : search
        }
        return render(request, 'pages/food_list.html', context)

    foods = Food.objects.all()
    best_food = Food.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')[:1]
    context = {
        'foods' : foods,
        'best_food' : best_food,
        }
    return render(request, 'pages/home.html', context)


def food_detail(request, slug):
    food = get_object_or_404(Food, slug=slug)
    feedbacks = FeedBack.objects.filter(food=food)
    recipe = Recipe.objects.filter(food=food).first()

    profile = get_object_or_404(Profile, user=food.user)
    if not profile:
        return HttpResponse('Page Not Found 404')

    if recipe:
        recipe.ingredients = recipe.ingredients.replace('.', '.<br>')
        recipe.instructions = recipe.instructions.replace('.', '.<br>')

    

        
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.food = food
            user.save()
        else:
            print(form.errors)
    else:
        form = FeedBackForm()

    context = {
        'food' : food,
        'form' : form,
        'feedbacks' : feedbacks,
        'recipe' : recipe,
        'profile' : profile
    }
    return render(request, 'pages/food_detail.html', context)


def premium(request):
    if request.user.is_authenticated:
        subscription, created = Subscription.objects.get_or_create(user=request.user, defaults={'end_date' : now() + timedelta(days=30) })
        if created and not subscription.is_active():
            subscription.end_date = now() + timedelta(days=30)
            subscription.save()
    return redirect('home')


def subscribe(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    subscription = getattr(request.user, 'subscription', None)
    if subscription and request.user.subscription.is_active():
        return redirect('home')
        
    return render(request, 'pages/premium.html')



def food_list(request):
    name = request.GET.get('category', None)
    categories = Category.objects.all()
    cuisines = Cuisine.objects.all()
    selected_cusine = request.GET.get('cuisine', None)
    if selected_cusine:
        cuisine = get_object_or_404(Cuisine, name=selected_cusine)
        if cuisine:
            foods = Food.objects.filter(cuisine=cuisine)
        else:
            foods = Food.objects.none()
    else:
        foods = Food.objects.all()

    # if name:
    #     category = get_object_or_404(Category, name=name)
    #     if category:
    #         foods = Food.objects.filter(category=category)
    #     else:
    #         foods = Food.objects.none()
    # else:
    #     foods = Food.objects.all()

    # if name:
    #     foods = Food.objects.filter(category__contains=categories)

    search = request.GET.get('search', '')
    if search:
        foods = Food.objects.filter(title__icontains=search)

    context = {
        'foods' : foods,
        'categories' : categories,
        'cuisines' : cuisines,
        'search' : search,
    }
    return render(request, 'pages/food_list.html', context)


@login_required
def add_food(request):

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        form_recipe = RecipeForm(request.POST, request.FILES)
        if form_recipe.is_valid and form.is_valid():
            # Save form but don't commit to DB yet
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            # Get category from form cleaned data instead of raw POST
            food.category = form.cleaned_data['category']
            recipe = form_recipe.save(commit=False)
            recipe.food = food
            recipe.save()
            
            return redirect('home')
    else:
        form = FoodForm()
        form_recipe = RecipeForm()
    return render(request, 'pages/add_food.html', {'form': form, 'form_recipe' : form_recipe})

@login_required
def update_food(request, slug):
    food = get_object_or_404(Food, slug=slug, user=request.user)
    recipe = get_object_or_404(Recipe, food=food)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        form_recipe = RecipeForm(request.POST, request.FILES)
        if form_recipe and form.is_valid():
            form.save()
            form_recipe.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = FoodForm(instance=food)
        form_recipe = RecipeForm(instance=recipe)
    return render(request, 'pages/update_food.html', {'form' : form, 'form_recipe' : form_recipe})

@login_required
def delete_food(request, slug):
    food = get_object_or_404(Food, slug=slug, user=request.user)
    food.delete()

@login_required
def like_view(request, slug):
    food = get_object_or_404(Food, slug=slug)
    if request.user in food.likes.all():
        food.likes.remove(request.user)
    else:
        food.likes.add(request.user)
    return redirect('home')

    
