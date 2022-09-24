from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import SignupForm
from .models import Record
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator


def home(request):
    data = Record.objects.all()
    return render(request, 'users/home.html', {'data': data})


@login_required
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            # raw_password = form.cleaned_data.get('password1')
            # log = form.cleaned_data.get('username')
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            login(request, stock.user, first_name)
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
    success_url = reverse_lazy('main-page')

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
    # permission_required = 'catalog.can_mark_returned'
    template_name = 'users/record_list_borrowed_all.html'


# def detail(request, rubric_pk, pk):
#     bb = get_object_or_404(Record, pk=pk)
#     ais = bb.additionalimage_set.all()
#     context = {'bb': bb, 'ais': ais}
#     return render(request, 'main/detail.html', context)
#

def main(request):
    data = Record.objects.all()
    return render(request, 'users/main.html', {'data': data})
