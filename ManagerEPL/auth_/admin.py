from django.contrib import admin
from django.contrib.admin import ModelAdmin
from auth_.models import MainUser, Profile

# Register your models here.

@admin.register(MainUser)
class MainUserAdmin(ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff')
    ordering = ('id',)


admin.site.register(Profile)
