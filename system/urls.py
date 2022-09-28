"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),

    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),

]

urlpatterns += [
    path(r'^record/(?P<pk>\d+)$', user_views.RecordDetailView.as_view(template_name='users/record_detail.html'),
         name='record-detail'),
    path(r'^record/create/$', user_views.RecordCreate.as_view(template_name='users/record_create.html'),
         name='record-create'),
    path(r'^record/(?P<pk>\d+)/delete/$', user_views.RecordDelete.as_view(template_name='users/record_delete.html'),
         name='record-delete'),
    path('my-records/', user_views.LoanedRecordsByUserListView.as_view(),
         name='my-records'),
    path('main/', user_views.main, name='main-page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
