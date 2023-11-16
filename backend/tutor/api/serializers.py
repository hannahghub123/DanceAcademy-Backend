from rest_framework.serializers import ModelSerializer
from tutor.models import *

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"      

class CourseStructSerializer(ModelSerializer):
    course = CourseSerializer() 
    class Meta:
        model = CourseStructure
        fields = "__all__"

    
class TutorSerializer(ModelSerializer):
    course = CourseSerializer(many=True) 
    class Meta:
        model = Tutor
        fields = "__all__"

class VideoUploadSerializer(ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = '__all__'

class ResumeListSerializer(ModelSerializer):
    class Meta:
        model = ResumeList
        fields = '__all__'