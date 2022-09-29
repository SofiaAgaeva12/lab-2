from django.contrib.auth.decorators import login_required
from django.http import Http404
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


from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class RecordDetailView(DetailView):
    model = Record
    template_name = 'users/record_detail.html'

    # def record_detail_view(request, pk):
    #     try:
    #         record_id = Record.objects.get(pk=pk)
    #     except Record.DoesNotExist:
    #         raise Http404("Record does not exist")
    #
    #     return render(request, 'users/record_detail.html', context={'record': record_id, })


class RecordCreate(CreateView):

    model = Record
    fields = ['title', 'summary', 'category', 'image']
    success_url = reverse_lazy('my-records')

    def form_valid(self, form):

        fields = form.save(commit=False)
        fields.user = self.request.user
        fields.save()
        return super().form_valid(form)


class StatusUpdate(UpdateView):
    model = Record
    template_name = 'users/status_update.html'
    fields = ['status']

    success_url = reverse_lazy('all-records')
    #
    # def form_valid(self, form):
    #
    #     fields = form.save(commit=False)
    #     fields.user = self.request.user
    #     fields.save()
    #     return super().form_valid(form)


class RecordDelete(DeleteView):
    model = Record
    success_url = reverse_lazy('my-records')
    template_name = 'users/record_delete.html'

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        record = super(RecordDelete, self).get_object(queryset)
        if record.status == 'n':
            if record.user != self.request.user:
                raise Http404(
                    "You don't own this object"
                )
            return record


class LoanedRecordsByUserListView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'users/record_list_user_all.html'

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs, )
        context['filter'] = RecordFilter(self.request.GET, queryset=self.get_queryset())
        return context


def main_context():
    counter = Record.objects.filter(status='a').count()
    data = Record.objects.all()
    context = {'data': data, 'counter': counter}
    return context


class MainView(ListView):

    model = Record
    template_name = 'users/main.html'
    paginate_by = 4

    def get_queryset(self):
        return Record.objects.order_by('created_at')

    def get_context_data(self, **kwargs):
        counter = Record.objects.filter(status='a').count()
        data = Record.objects.all()
        context = {'data': data, 'counter': counter}
        return context


class AllRecordsView(ListView):

    model = Record
    template_name = 'users/all_records.html'

    def get_queryset(self, **kwargs):
        return Record.objects.order_by('created_at')

    def get_context_data(self, **kwargs):
        data = Record.objects.all()
        context = {'data': data}
        return context



