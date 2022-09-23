from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from .models import Record
from django.core.files.storage import FileSystemStorage


def home(request):
    data = Record.objects.all()
    return render(request, 'users/home.html', {'data': data})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
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


from django.views.generic import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin


class RecordCreate(CreateView):
    model = Record
    fields = ['title', 'summary', 'category', 'image']


class LoanedRecordsByUserListView(PermissionRequiredMixin, ListView):
    model = Record
    # permission_required = 'catalog.can_mark_returned'
    template_name = 'users/record_list_borrowed_all.html'


def main(request):
    data = Record.objects.all()
    return render(request, 'users/main.html', {'data': data})
