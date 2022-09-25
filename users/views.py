from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import SignupForm
from .models import Record
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from .filters import RecordFilter


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
    success_url = reverse_lazy('my-records')

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.user = self.request.user
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)


class LoanedRecordsByUserListView(PermissionRequiredMixin, ListView):
    model = Record
    template_name='users/record_list_user_all.html'
    # paginate_by = 4

    def get_queryset(self):
        return Record.objects.filter(orderer=self.request.user).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs,)
        context['filter'] = RecordFilter(self.request.GET, queryset=self.get_queryset())
        return context


def main(request):
    data = Record.objects.all()
    return render(request, 'users/main.html', {'data': data})
