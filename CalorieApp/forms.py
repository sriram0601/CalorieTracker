from django import forms
from .models import Profile,Food
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#Create Form From Here

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class SelectFoodForm(forms.ModelForm):
    def __init__(self,user,*args,**kwargs):
        super(SelectFoodForm,self).__init__(*args,**kwargs)
        self.fields['food_selected'].queryset = Food.objects.filter(person_of = user)

    class Meta:
        model = Profile
        fields = ['food_selected','quantity']
    

class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name','quantity','calories')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('calorie_goal',)
    