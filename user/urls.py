from django.urls import path
from .views import UserRegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user'),
   
    # path('token/', UserRegisterView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
