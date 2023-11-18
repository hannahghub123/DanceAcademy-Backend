from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(CourseStructure)
admin.site.register(VideoUpload)
admin.site.register(ResumeList)
