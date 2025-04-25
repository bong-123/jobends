from django.urls import path
from .views import CompanyByJobCategoryView


from .views import (
   
    CompanyListCreateView, CompanyDetailView,
   
    PositionListCreateView, PositionDetailView
)

urlpatterns = [


    # Position Endpoints
    path('positions/', PositionListCreateView.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),

    # Company Endpoints
    path('companies/by-category/<str:jobcategory>/', CompanyByJobCategoryView.as_view(), name='company-by-category'),
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    


]
