from django.contrib import admin
from .models import Profile, Category
from .models import Record

admin.site.register(Profile)

admin.site.register(Record)
admin.site.register(Category)
