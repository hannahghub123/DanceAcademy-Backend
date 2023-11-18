from django.urls import path
from .views import *

urlpatterns = [
    path("adminlogin/",AdminLoginView.as_view(),name="adminlogin"),
    path("count/",Totalcount.as_view(),name="total-count"),
    path("tutor-uploads/",TutorUploads.as_view(),name="tutor-uploads"),
]
