from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailFormUpdate

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('profile/email/', EmailFormUpdate.as_view(), name='profile_email'),
]