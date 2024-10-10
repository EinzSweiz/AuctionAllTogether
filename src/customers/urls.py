from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('update_profile/', views.UpdateProfile.as_view(), name='update_profile'),
]