from django import forms
from .models import Food, Recipe, FeedBack

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('category', 'title', 'slug', 'description', 'story','thumbnail', 'cuisine','img')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('ingredients' , 'instructions', 'cooking_time', 'image', 'video')

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('comment',)