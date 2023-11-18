from django.urls import path
from .views import *

urlpatterns = [
    path("signup/",SignupView.as_view(),name="signup"),
    path("resume-upload/",ResumeUploadView.as_view(),name="resume-upload"),
    path("login/",LoginView.as_view(),name="login"),
    path("tprofedit/",ProfileEditView.as_view(),name="edit-profile"),
    path("courses/",CourseView.as_view(),name="course"),
    path("course-details/<int:id>",CourseDetailsView.as_view(),name="course-details"),
    path("course-struct/<int:id>",CourseStructView.as_view(),name="course-struct"),
    path("course-structure/",CourseStructureView.as_view(),name="course-structure"),
    path("course-struct/",StructDetailsView.as_view(),name="struct-details"),
    path("image-set/",ImageSetView.as_view(),name="image-setting"),
    path("tdetails/<int:id>",TutorView.as_view(),name="tutor-view"),
    path("video-upload/<int:id>",VideoUploadView.as_view(),name="video-upload"),
    path("video-lists/",VideoListsView.as_view(),name="video-lists"),
    path("tutor-details/",TutorDetailsView.as_view(),name="tutor-details"),
    path("status-edit/",StatusEditView.as_view(),name="status-edit"),
    path("admincourse-edit/",AdminCourseEditView.as_view(),name="admincourse-edit"),
    path("course-structedit/",CourseStructEditView.as_view(),name="course-structedit"),
    path("courseImage-set/",CourseImageSetView.as_view(),name="courseImage-set"), 
    path("pay-details/",PayDetailsView.as_view(),name="pay-details"),
    path("task-details/",TaskDetailsView.as_view(),name="task-details"),
    path("task-edit/",TaskEditView.as_view(),name="task-edit"),
    path("task-delete/",TaskDeleteView.as_view(),name="task-delete"),
    path("get-task/",GetTaskView.as_view(),name="get-task"),
    path('add-course/',AddCourseView.as_view(),name="add-course")
]