from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=100,null=False)
    quantity = models.IntegerField(default=0,null=False)
    calories = models.FloatField(null=False,default=0)
    person_of = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    person_of = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    calorie_count = models.FloatField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True)
    total_calories = models.FloatField(default=0,null=False)
    calorie_goal = models.FloatField(default=100,null=True,blank=False)
    date = models.DateTimeField(default=timezone.now())
    food_selected = models.ForeignKey(Food,on_delete=models.CASCADE,null=True,blank=True)
    all_selected_food_today = models.ManyToManyField(Food,related_name='invertory')

    def save(self,*args,**kwargs):
        if (self.food_selected != None):
            self.amount = (self.food_selected.calories / self.food_selected.quantity)
            self.calories = self.amount*self.quantity
            self.total_calories = self.calorie_count + self.total_calories
            calories = Profile.objects.filter(person_of = self.person_of).last()

            PostFood.objects.create(profile=calories,
                                    food=self.food_selected,
                                    calories_amount=self.calories,
                                    amount=self.quantity)
            self.food_selected=None
            super(Profile, self).save(*args,**kwargs)
        else:
            super(Profile, self).save(*args,**kwargs)

    def __str__(self):
        return (self.person_of.username)

class PostFood(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    calories_amount  = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    

