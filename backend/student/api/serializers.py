from rest_framework.serializers import ModelSerializer
from student.models import *
from tutor.api.serializers import *

class StudentSerializer(ModelSerializer):
    course = CourseSerializer() 
    class Meta:
        model = Student
        fields = "__all__"


class CoursePaymentSerializer(ModelSerializer):
    structId = CourseStructSerializer() 
    studentId = StudentSerializer() 
    tutorId = TutorSerializer() 
    class Meta:
        model = CoursePayment
        fields = "__all__"

class MyNotesSerializer(ModelSerializer):
    student = StudentSerializer() 
    class Meta:
        model = MyNotes
        fields = "__all__"

class SessionAssignSerializer(ModelSerializer):
    student = StudentSerializer() 
    tutor = TutorSerializer() 
    course_struct = CourseStructSerializer() 
    class Meta:
        model = SessionAssign
        fields = "__all__"

class ActivityAssignSerializer(ModelSerializer):
    session_assign = SessionAssignSerializer()
    class Meta:
        model = ActivityAssign
        fields = "__all__"

class TaskUploadSerializer(ModelSerializer):
    student = StudentSerializer()
    task = ActivityAssignSerializer
    class Meta:
        model = TaskUpload
        fields = "__all__"