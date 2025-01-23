from django.contrib import admin
from .models import Food, Recipe, FeedBack, Subscription, Category, Cuisine

# Register your models here.


admin.site.register(Food)
admin.site.register(Recipe)
admin.site.register(FeedBack)
admin.site.register(Subscription)
admin.site.register(Category)
admin.site.register(Cuisine)