from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken 
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from student.models import *
from tutor.models import *
from student.api.serializers import *
from tutor.api.serializers import *
from .serializers import *


class AdminLoginView(APIView):
    def post(self,request):
        print("HELLOOO")
        username = request.data.get("username")
        password = request.data.get("password")
        print(username,password)

        try:
            adminobj = User.objects.get(username=username)
            print(adminobj,"????????????????")
            if check_password(password, adminobj.password):
                refresh = RefreshToken.for_user(adminobj)
                print(refresh,'##############')
                stdobjs = Student.objects.all()
                tobjs = Tutor.objects.all()
                stdserialized = StudentSerializer(stdobjs, many=True)
                tutorserialized = TutorSerializer(tobjs,many=True)
                adminserialized = AdminSerializer(adminobj)
                return Response({'message':'Login Success','adminaccess': str(refresh.access_token), 'adminrefresh':str(refresh),'adminData':adminserialized.data, 'stdData':stdserialized.data, 'tutorData':tutorserialized.data})
            else:
                return Response({'message':"Invalid credentials"})
            
        except:
            return Response({'message':'user not found'})
        
class Totalcount(APIView):
    def post(self,request):

        stdobj = Student.objects.all()
        tutorobj = Tutor.objects.all()
        courseobj = Course.objects.all()
        tutorupload = VideoUpload.objects.all()
        stdupload = TaskUpload.objects.all()
        taskobj = ActivityAssign.objects.all()
        feedbackobj = Feedbacks.objects.all()

        tutorUploadcount = tutorupload.count()
        stdUploadcount = stdupload.count()
        taskCount = taskobj.count()
        stdCount = stdobj.count()
        tutorCount = tutorobj.count()
        courseCount = courseobj.count() 
        feedbackCount = feedbackobj.count()

        return Response({"stdCount":stdCount,"tutorCount":tutorCount,"courseCount":courseCount,"stdUploadcount":stdUploadcount,"tutorUploadcount":tutorUploadcount,"taskCount":taskCount,"feedbackCount":feedbackCount})
    
class TutorUploads(APIView):
    def post(self,request):
        tutorupload = VideoUpload.objects.all()
        serialized = VideoUploadSerializer(tutorupload,many=True)

        return Response(serialized.data)

