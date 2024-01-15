from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import  EditUserForm ,RegisterUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Dashboard.utils import get_counts
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Username and password are required.")
    
    return render(request, 'authentication/login.html')



def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful")
                return redirect('login')
            else:
                form = RegisterUserForm()
        
    return render(request, 'registration/register.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out")
    return redirect('login')
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, "Registration successful")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors in the form.")
    else:
        form = RegisterUserForm()
    
    return render(request, 'authentication/register.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    counts = get_counts()
    return render(request, 'profile/user_profile.html', {'user': user,**counts})


@login_required
def view_user(request):
    user= User.objects.all()
    counts = get_counts()
    return render(request,'profile/view_user.html',{'user':user,**counts})

@login_required
def modify_user(request, pk):
    user = get_object_or_404(User,pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"User Profile odified Successfully!  ")
            return redirect('view_user')  # Redirect to the user table view after modification
    else:
        form = EditUserForm(instance=user)
    counts = get_counts()
    return render(request, 'profile/modify_user.html', {'form': form,**counts})

def delete_user(request, pk):
    delete_user= User.objects.get(id=pk)
    delete_user.delete()
    delete_user.is_deleted = True
    messages.success(request,"Product Record is deleted Successfully  ")
    return redirect('view_user')