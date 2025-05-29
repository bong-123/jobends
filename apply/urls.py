from django.urls import path
from .views import ApplyView, UpdateApplicationStatusView, UserApplicationsView

urlpatterns = [
    path('apply/', ApplyView.as_view(), name='apply'),
    path('applications/<int:application_id>/status/', UpdateApplicationStatusView.as_view(), name='update_application_status'),
    path('user-applications/', UserApplicationsView.as_view(), name='user_applications'),
]