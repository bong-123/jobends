from django.contrib import admin
from .models import CustomUser

class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'username', 'email')
    search_fields = ('last_name', 'username', 'email')
    list_per_page = 10
# Register your models here.
admin.site.register(CustomUser, CustomUserModelAdmin)