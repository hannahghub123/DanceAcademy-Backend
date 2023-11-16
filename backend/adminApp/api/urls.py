from django.urls import path
from .views import *

urlpatterns = [
    path("adminlogin/",AdminLoginView.as_view(),name="adminlogin")
]
