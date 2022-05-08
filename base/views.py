from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, hashers, logout as auth_logout
from base.forms import LogInForm, SignUpForm
from base.models import User


def index(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST, request.POST)
        if form.is_valid():
            email = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, "Login successful.")
                return redirect('/')
            else:
                messages.info(request, "Invalid.")

    form = LogInForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.info(request, "Logout successful.")
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not User.objects.filter(email=email).exists():
                form.save()
                messages.info(request, "Account created successfully.")
                return redirect('/login')
            else:
                messages.info(request, "E-mail already exists.")

    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def categories(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'categories.html', context)


def dashboard(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'dashboard.html', context)


def cart(request):
    context = {'login': False}
    user = request.user
    if user.is_authenticated:
        context = {'login': True}
    return render(request, 'cart.html', context)
