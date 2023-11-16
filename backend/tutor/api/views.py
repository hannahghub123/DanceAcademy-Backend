from rest_framework.views import APIView
from tutor.models import *
from student.models import *
from .serializers import *
from student.api.serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from cloudinary.uploader import upload
import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary import api


cloudinary.config(
    cloud_name="dhclqk43b",
    api_key="518455332798936",
    api_secret="B9sKOi_eENWKswo6l2j_kCaBxIs",
)

class SignupView(APIView):
    def post(self,request):
        username=request.data.get("username")
        name=request.data.get("name")
        expertise = request.data.get("expertise")
        qualification = request.data.get("qualification")
        email=request.data.get("email")
        password=request.data.get("password")
        phone=request.data.get("phone")
        courses = request.data.get("courses") 
        # resume = request.FILES.get("resume")

        print("heyy tutor>>>>>>>>>>")

        tobj=Tutor.objects.create(username=username,name=name,expertise=expertise,qualification=qualification,email=email,phone=phone,password=password)
        if courses:
            courseobj = Course.objects.filter(title__in=courses)
            tobj.course.set(courseobj)
            print(tobj,"hii i am hereee")
        

        serialized = TutorSerializer(tobj)
       

        return Response({"data":serialized.data,"message":"success"})
    
class ResumeUploadView(APIView):
    def post(self,request):
        id = request.data.get("id")
        print("id////////",id)
        resume = request.data.get("resume")
        print("Resumeeeeeee",resume)
        tobj = Tutor.objects.get(id=id)
        print(tobj,"<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>tobjjjj")

        # if not resume.content_type.startswith('application/pdf'):
        #     print("errorrr////")
        #     return Response({'error': 'File must be a PDF document'})


        upload_result = cloudinary.uploader.upload(resume, resource_type="auto", folder="DanceAcademy/resume-uploads")
        resobj = ResumeList(
        res_file=upload_result['secure_url'],  
        up_time=timezone.now(),

        )
        resobj.save()
        resobj.tutors.add(tobj)
        print(">>>>>>>>>>>","url",resobj.res_file)

        
        return Response({'url': resobj.res_file}) 

    

class LoginView(APIView):
    def post(self,request):
        
        email=request.data.get("email")
        password=request.data.get("password")
        try:
            tobj = Tutor.objects.get(email=email, password=password)
            refresh = RefreshToken.for_user(tobj)
            serialized = TutorSerializer(tobj)
            id = tobj.id
            print(tobj.id,">>>>>>>>>>>>>>>>>>...iddddd")
            if tobj.is_approved:
                return Response({"id":id,"message":"success","data":serialized.data, "refresh":str(refresh),"access":str(refresh.access_token)})
            else:
                return Response({"id":id,"message":"not approved"})
                
        except:

            return Response({"message":"Invalid credentials"})
        

class ProfileEditView(APIView):
    def post(self,request):
        id = request.data.get("id")
        print(id,"id vannu>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        username=request.data.get("username")
        name=request.data.get("name")
        expertise = request.data.get("expertise")
        qualification = request.data.get("qualification")
        email=request.data.get("email")
        password=request.data.get("password")
        phone=request.data.get("phone")

        print("heyy tutor edit profilee>>>>>>>>>>",id,username,name,expertise,qualification,email,phone,password)

        tobj = Tutor.objects.get(id=id)
        print("??????????????",tobj.name)
        tobj.username = username
        tobj.name = name
        tobj.expertise = expertise
        tobj.qualification = qualification
        tobj.email = email
        tobj.phone = phone
        tobj.password = password
        tobj.save()
        serialized = TutorSerializer(tobj)

        return Response(serialized.data)
            
    
class CourseView(APIView):
    def get(self,request):
        cobj = Course.objects.all()
        serialized = CourseSerializer(cobj,many=True)

        return Response(serialized.data)
    
class AdminCourseEditView(APIView):
    def post(self,request):
        id = request.data.get("id")
        title = request.data.get("title")
        description = request.data.get("description")

        print(id,title,description)

        courseobj = Course.objects.get(id=id)
        print(courseobj,"beforee")
        courseobj.title=title
        courseobj.description=description
        courseobj.save()

        courseobj = Course.objects.get(id=id)
        print(courseobj,"updated")
        serialized = CourseSerializer(courseobj)
        return Response(serialized.data)
    
class CourseStructView(APIView):
    # from admin side 
    def get(self,request,id):
        cobj = Course.objects.get(id=id)
        print(id,cobj,"MMMMMMMMMMMMMMMM")
        structobj = CourseStructure.objects.filter(course=cobj)
        serialized = CourseStructSerializer(structobj,many=True)

        return Response(serialized.data) 
    

class CourseStructEditView(APIView):
    def post(self,request):
        id = request.data.get("id")
        title = request.data.get("title")
        levels = request.data.get("levels")
        price =  request.data.get("price")
        description = request.data.get("description")
        duration = request.data.get("duration")
        num_of_classes = request.data.get("num_of_classes")
        price_per = request.data.get("price_per")

        structobj = CourseStructure.objects.get(id=id)
        structobj.title = title
        structobj.levels = levels
        structobj.price = price
        structobj.description = description
        structobj.duration=duration
        structobj.num_of_classes=num_of_classes
        structobj.price_per=price_per
        structobj.save()

        structobj = CourseStructure.objects.get(id=id)
        serialized = CourseStructSerializer(structobj)
        return Response(serialized.data)

class CourseStructureView(APIView):
    def post(self,request):
        id = request.data.get("id")
        cobj = Course.objects.get(id=id)
        print(id,cobj,"MMMMMMMMMMMMMMMM")
        structobj = CourseStructure.objects.filter(course=cobj)
        serialized = CourseStructSerializer(structobj,many=True)
        print(serialized.data,"heyy haha")
        return Response(serialized.data)
    
class StructDetailsView(APIView):
    def post(self,request):
        id = request.data.get("id")
        structobj = CourseStructure.objects.get(id=id)
        serialized = CourseStructSerializer(structobj)
        print(serialized.data,"heyy haha")
        return Response(serialized.data)
    
class CourseDetailsView(APIView):
    def get(self,request,id):
        cobj = Course.objects.get(id=id) 
        serialized = CourseSerializer(cobj)

        return Response(serialized.data)
    
    
class TutorView(APIView):
    def get(self,request,id):
        cobj = Course.objects.get(id=id) 
        tobj = Tutor.objects.filter(course=cobj)
        print(tobj,"$tutor obj",cobj)
        serialized = TutorSerializer(tobj,many=True)

        return Response(serialized.data)
    
class TutorDetailsView(APIView):
    def get(self,request):
        tutorobjs = Tutor.objects.all()
        serialized = TutorSerializer(tutorobjs,many=True)

        return Response(serialized.data)
    
class StatusEditView(APIView):
    def post(self,request):
        id=request.data.get("id")
        tutorobj = Tutor.objects.get(id=id)

        if tutorobj.is_approved == True:
            tutorobj.is_approved=False
            message = "restricted"
        else:
            tutorobj.is_approved=True
            message="approved"

        tutorobj.save()

        # serialized = TutorSerializer(tutorobj)

        return Response({"message":message})
    
class ImageSetView(APIView):
    def post(self,request):
        id=request.data.get("id")
        image=request.data.get("image")
        print(image,"Kuiii",id)

        tobj= Tutor.objects.get(id=id)
        tobj.image=image
        tobj.save()

        serialized = TutorSerializer(tobj)
        return Response({"message":"success","data":serialized.data})
    
class CourseImageSetView(APIView):
    def post(self,request):
        id=request.data.get("id")
        image=request.data.get("image")
        print(image,"course Kuiii",id)

        course_obj= Course.objects.get(id=id)
        course_obj.image=image
        course_obj.save()

        serialized = CourseSerializer(course_obj)
        return Response(serialized.data)


class VideoUploadView(APIView):
    # parser_classes = (FileUploadParser,)

    def post(self, request,id):
        # if 'file' not in request.data:
        #     return Response({'error': 'No file part'})

        file = request.data.get("video")

        tobj = Tutor.objects.get(id=id)
        print(tobj,"?????????????tobj ")

        if file.content_type.split('/')[0] != 'video':
            return Response({'error': 'File must be a video'})

        # Create a Video_upload instance with the Cloudinary URL
        result = upload(file, resource_type="video",folder="DanceAcademy/video-uploads")

        video_upload = VideoUpload(
            v_upload=result['secure_url'],  # Store the Cloudinary URL
            up_time=timezone.now(),
            desc=request.data.get('description', '') 
        )
        
        video_upload.save()
        video_upload.tutors.add(tobj)
        return Response({'url': video_upload.v_upload})

class VideoListsView(APIView):
    def post(self, request):
        tutor_id = request.data.get("id")
        print(tutor_id,"id hey")
        try:
            tobj = Tutor.objects.get(id=tutor_id)
        except Tutor.DoesNotExist:
            return Response({"error":"Tutor not found"})
        

        videos = VideoUpload.objects.filter(tutors=tobj)
        print(videos,"####@@@@@@@2")


        # video_resources = api.resources(type="upload", prefix="DanceAcademy/", resource_type="video")

        video_urls = [
            {
                'v_upload':video.v_upload.url,
                'up_time':video.up_time,
                'desc':video.desc,
            }
            for video in videos
        ]

        uploadCount =  len(video_urls)
        print(uploadCount,"*********")


        return Response({"message":"success","video_urls":video_urls,'uploadCount':uploadCount})

        
class PayDetailsView(APIView):
    def post(self,request):
        totalCount = 0
        tutorId = request.data.get("id")
        print(tutorId,"&&&")

        payobj = CoursePayment.objects.filter(tutorId_id=tutorId)
        print(payobj.values(),"#########3")
        
        totalCount = len(payobj)

        serialized = CoursePaymentSerializer(payobj,many=True)

        return Response({"paydata":serialized.data,'totalCount':totalCount})

