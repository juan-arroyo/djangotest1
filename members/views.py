from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from . forms import RegisterUserForm


# LOGIN USER
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'There was an error Loggin in, try again ...')
            return redirect('login')
            

    else:
        context = {}
        return render(request, 'members/authenticate/login.html', context)


# LOGOUT USER
def logout_user(request):
    logout(request)
    messages.success(request, 'You were Logged Out !')
    return redirect('login')

# CREATE USER
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration Successful!')
            return redirect('home')

    else:
        form = RegisterUserForm()
    context = {'form':form}
    return render(request, 'members/authenticate/register_user.html', context)