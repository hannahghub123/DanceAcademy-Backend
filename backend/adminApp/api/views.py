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
