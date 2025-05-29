from django.urls import path

from .views import (
    PositionListCreateView, PositionDetailView,
    EmployeePositionListCreateView, EmployeePositionDetailView,
    CompanyListCreateView, CompanyDetailView, CompanyByJobCategoryView
)

urlpatterns = [
    # Position Endpoints
    path('positions/', PositionListCreateView.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),

    # EmployeePosition Endpoints
    path('employee-positions/', EmployeePositionListCreateView.as_view(), name='employee-position-list-create'),
    path('employee-positions/<int:pk>/', EmployeePositionDetailView.as_view(), name='employee-position-detail'),

    # Company Endpoints
    path('companies/by-category/<str:jobcategory>/', CompanyByJobCategoryView.as_view(), name='company-by-category'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
]