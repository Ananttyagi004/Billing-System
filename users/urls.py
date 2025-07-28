from django.urls import path
from .views import RegisterView, LoginView, CustomerProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
]
