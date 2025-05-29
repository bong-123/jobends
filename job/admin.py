from django.contrib import admin
from .models import Company, Position, EmployeePosition

class EmployeePositionInline(admin.TabularInline):
    model = EmployeePosition
    extra = 1

class PositionModelAdmin(admin.ModelAdmin):
    list_display = ('jobcategory',)
    search_fields = ('jobcategory',)
    list_per_page = 10
    inlines = [EmployeePositionInline]  # Show related employee positions inline

class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_position_category', 'location', 'employee_position')
    search_fields = ('name', 'location', 'employee_position__title', 'employee_position__position__jobcategory')
    list_per_page = 10

    def get_position_category(self, obj):
        return obj.employee_position.position.jobcategory
    get_position_category.short_description = 'Job Category'

# Register models
admin.site.register(Position, PositionModelAdmin)
admin.site.register(EmployeePosition)
admin.site.register(Company, CompanyModelAdmin)