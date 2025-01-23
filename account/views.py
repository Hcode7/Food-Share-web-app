from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from app.models import Subscription, Food
from .forms import UserProfile
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=request.user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form' : form})\

@login_required
def profile(request):
    search = request.GET.get('search')
    if search:
        foods = Food.objects.filter(title__icontains=search)

        context = {
            'foods' : foods,
            'search' : search,
        }
        return render(request, 'registration/profile.html', context)
    
    foods = Food.objects.filter(user=request.user)
    context = {
        'foods' : foods,
    }
    return render(request, 'registration/profile.html', context)


@login_required
def channel(request, username):
    profile = get_object_or_404(Profile, username=username)
    foods = Food.objects.filter(user=profile.user)

    context = {
        'profile' : profile,
        'foods' : foods,
        'current_user ' : request.user
    }
    return render(request, 'registration/channel.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')
