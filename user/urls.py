from django.urls import path

from .views import registerUser


app_name = "user"

urlpatterns = [
    path('register/', registerUser, name='register'),
]
