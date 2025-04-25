from django.contrib import admin
from .models import  Company, Position

class PositionModelAdmin(admin.ModelAdmin):
    list_display = ('jobcategory', 'title')
    search_fields = ('jobcategory', 'title')
    list_per_page = 10

class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'location')
    search_fields = ('position', 'name', 'location')
    list_per_page = 10
# Register your models here.
admin.site.register(Position, PositionModelAdmin)
admin.site.register(Company, CompanyModelAdmin)
