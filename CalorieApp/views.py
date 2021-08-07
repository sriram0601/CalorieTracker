from .filters import FoodFilter
from django.utils import timezone
from django.contrib import messages
from .models import Food, PostFood,Profile
from django.shortcuts import render,redirect
from datetime import datetime,date,timedelta
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm,SelectFoodForm,AddFoodForm


# Create your views here.

@login_required()
def homePage(request):
    
    #Looking For latest profile object 
    calories = Profile.objects.filter(person_of = request.user).last()
    calorie_goal = calories.calorie_goal
    if calorie_goal == None:
        calorie_goal = 100.0
    #creating One profile for each day
    print(f'#############\nCalorie-Date: {calories.date}\nDate-Today: {date.today()}\nTimezone-now: {timezone.now()}\n##########')
    if timezone.now() > calories.date:
        profile=Profile.objects.create(person_of=request.user)
        profile.save()
    
    #If new Profile is created,we need to update our last profile...
    calories = Profile.objects.filter(person_of = request.user).last()

    #Showig all food consumed on day
    all_food_today = PostFood.objects.filter(profile=calories)
    print(f'{"####"*5}\ncalorie_goal : {calorie_goal}\nTotal-calorie: {calories.total_calories}\n{"####"*5}')
    calorie_goal_status = calorie_goal-calories.total_calories

    over_calorie = 0
    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)
    
    context = {
        'total_food' : all_food_today,
        'over_calorie' : over_calorie,
        'calorie_goal' : calorie_goal,
        'total_calorie' : calories.total_calories,
        'calorie_goal_status' : calorie_goal_status,
    }

    return render(request,'home.html',context)


#View For Registration
def registrationPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get['username']
                messages.success(request,'Account successfully created for ',username)
                return redirect('home')
            else:
                messages.warning(request,'Error occurred, While creating the account')
                return redirect('register')
        context={'form':form}
        return render(request,'register.html',context)

#Create login page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.cleaned_data.get['username']
            password = request.cleaned_data.get['password']

            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,username=username,password=password)
                return redirect('home')
            else:
                messages.info(request,'Username or password is incorrect')
        context={}
        return render(request,'login.html',context)

#Create a Logout view
def logoutPage(request):
    logout(request)
    return redirect('login')

#From Here we have to create CRUD operations
def selectFoodPage(request):
    person = Profile.objects.filter(person_of=request.user).last()
    food = Food.objects.filter(person_of=request.user)
    form = SelectFoodForm(request.user,instance=person)

    if request.method == 'POST':
        form = SelectFoodForm(request.user,request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = SelectFoodForm(request.user)
    context={'form':form,
            'food':food}
    return render(request,'selectFood.html',context)

#Add Food in a page
def addFoodPage(request):
    food_items = Food.objects.filter(person_of=request.user)
    form = AddFoodForm(request.POST)
    
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.person_of = request.user
            profile.save()
            return redirect('addFood')
        else:
            form = AddFoodForm()

        #Filter the Food
    myFilter = FoodFilter(request.GET,queryset=food_items)
    food_items = myFilter.qs
    context = {
        'form':form,
        'food_items':food_items,
        'myFilter':myFilter,
    }
    return render(request,'addFood.html',context)

#Update the Food items
@login_required
def updateFood(request,pk):
    food_items = Food.objects.filter(person_of=request.user)
    food_item = Food.objects.get(pk=pk)
    form = AddFoodForm(food_item)

    if request.method == 'POST':
        form = AddFoodForm(request.POST,instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('profile')
    myFilter = FoodFilter(request.GET,queryset=food_items)
    context = {
        'form':form,
        'myfilter' : myFilter,
        'food_items':food_items,
    }
    return render(request,'addFood.html',context)

#Delete Food items
@login_required
def deleteFoodPage(request,pk):
    food_item = Food.objects.get(pk=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('profile')
    context = {'food_item':food_item}
    return render(request,'deleteFood.html',context)

#Deals With Profile page
def profilePage(request):
    person = Profile.objects.filter(person_of = request.user).last()
    food_item = Food.objects.filter(person_of=request.user)
    form = ProfileForm(instance=person)

    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=person)

        #Query the records for last 7 days
    last_week = timezone.now() - timedelta(days=7)
    records = Profile.objects.filter(
                                    date__gte=last_week,
                                    date__lt=timezone.now().date(),
                                    person_of=request.user
                                )
    context={
        'form':form,
        'food_item':food_item,
        'record':records
    }
    return render(request,'profile.html',context)