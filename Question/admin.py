from django.contrib import admin

from .models import User


# Register your models here.


@admin.register(User)
class register_user(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'score']
    ordering = ['-created_time']
    search_fields = ['first_name']
    list_filter = ['score', 'created_time']