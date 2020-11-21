from django.contrib import admin
from .models import Permission, Role, UserRole
models = [Permission, Role, UserRole]
# Register your models here.
admin.site.register(models)
