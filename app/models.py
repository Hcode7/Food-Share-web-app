from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Cuisine(models.Model):
    CUISINE_CHOICES = [
        ('Moroccan', 'Moroccan'),
        ('Italien', 'Italien'),
        ('Japanese' , 'Japanes'),
        ('USA' , 'USA')
    ]
    name = models.CharField(max_length=150, choices=CUISINE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
        ('Dessert', 'Dessert'),
    ]
    name = models.CharField(max_length=150, choices=CATEGORY_CHOICES)
    slug = models.CharField(max_length=150 , blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categories"

class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=500)
    story = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_recipe', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnail/')
    img = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Recipe(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    is_premium = models.BooleanField(default=False)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    video = models.FileField(upload_to='media/',blank=True, null=True)

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date > self.start_date
    
    def __str__(self):
        return f'Subscription for {self.user.username}'


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


