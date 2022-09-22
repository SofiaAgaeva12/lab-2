from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm


def home(request):
    return render(request, 'users/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            first_name = form.cleaned_data.get('first_name')
            raw_password = form.cleaned_data.get('password1')
            log = form.cleaned_data.get('username')
            user = authenticate(username=log, password=raw_password)
            login(request, user, first_name)
            return redirect('home')
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'users/signup.html', context)
