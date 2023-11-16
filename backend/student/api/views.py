from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from tutor.api.serializers import *
from django.conf import settings
from student.models import *
from .serializers import *
from cloudinary import api
import string
import random

from cloudinary.uploader import upload
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="dhclqk43b",
    api_key="518455332798936",
    api_secret="B9sKOi_eENWKswo6l2j_kCaBxIs",
)


class SignupView(APIView):
    def post(self,request):
        username=request.data.get("username")
        name=request.data.get("name")
        # score=request.data.get("score")
        email=request.data.get("email")
        password=request.data.get("password")
        repassword=request.data.get("repassword")
        phone=request.data.get("phone")
        
        if password==repassword:
            Student.objects.create(username=username,name=name,email=email,phone=phone,password=password)
            stdobj = Student.objects.get(username=username)
            serialized = StudentSerializer(stdobj)

            return Response({"message":"success" ,"data":serialized.data})
        
        else:
            return Response({"error":"passwords doesn't match"})
    

class LoginView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        try:
            stdobj = Student.objects.get(username=username, password=password)
            refresh = RefreshToken.for_user(stdobj)
            serialized = StudentSerializer(stdobj)
            return Response({"message":"success","data":serialized.data, "refresh":str(refresh),"access":str(refresh.access_token)})
                
        except:

            return Response({"message":"Invalid credentials"})
        
class StudentDetailsView(APIView):
    def get(self,request):
        studentobj = Student.objects.all()
        serialized = StudentSerializer(studentobj,many=True)

        return Response(serialized.data)
            
        
class ImageSetView(APIView):
    def post(self, request):
        id=request.data.get("id")
        image=request.data.get("image")
        # print(image,"Kuiii",id)

        sobj= Student.objects.get(id=id)
        sobj.image=image
        sobj.save()

        serialized = StudentSerializer(sobj)
        return Response({"message":"success","data":serialized.data})

class ProfileEditView(APIView):
    def post(self,request):
        id = request.data.get("id")
        print(id,"id vannu>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        username=request.data.get("username")
        name=request.data.get("name")
        score = request.data.get("score")
        course = request.data.get("course")
        email=request.data.get("email")
        password=request.data.get("password")
        phone=request.data.get("phone")
        cobj = Course.objects.get(id=course)
        print("heyy std edit profilee>>>>>>>>>>",id,username,name,score,email,phone,password,"???????",course,"???????????????")

        try:
            stdobj = Student.objects.get(id=id)
            stdobj.username = username
            stdobj.name = name
            stdobj.score = score
            stdobj.course = cobj 
            stdobj.email = email
            stdobj.phone = phone
            stdobj.password = password
            stdobj.save()

            # c_serialized = CourseSerializer(stdobj.course), "course": c_serialized.data}
            serialized = StudentSerializer(stdobj)
            print(serialized.data,"hi data")
            return Response({"data": serialized.data} )
        except Student.DoesNotExist:
            return Response({"error": "Student not found"})

class VideoListView(APIView):
    def post(self,request):
        tutor_id = request.data.get("id")
        print(tutor_id,":???????>>>>>>>>>>>>")
        try:
            tobj = Tutor.objects.get(id=tutor_id)
        except Tutor.DoesNotExist:
            return Response({"error":"Tutor not found"})
        

        videos = VideoUpload.objects.filter(tutors=tobj)
        print(videos,"####@@@@@@@in stddd")

        video_urls = [
            {
                'v_upload':video.v_upload.url,
                'up_time':video.up_time,
                'desc':video.desc,
            }
            for video in videos
        ]


        return Response({"message":"success","video_urls":video_urls})


class CoursePaymentView(APIView):
    def post(self,request):
        studentId = request.data.get("studentId")
        structId = request.data.get("structId")
        tutorName = request.data.get("tutorName")
        razorpayId = request.data.get("razorpayId")

        stdobj = Student.objects.get(id=studentId)
        structobj = CourseStructure.objects.get(id=structId)
        tobj = Tutor.objects.get(name=tutorName)

        payobj = CoursePayment.objects.create(
            studentId=stdobj,
            structId=structobj,
            tutorId=tobj,
            razorpayId=razorpayId
        )

        print(payobj,"MJJJJJJJJJJJ")

        serialized = CoursePaymentSerializer(payobj)
        return Response(serialized.data)

class PayDetailsView(APIView):
    def post(self,request):
        tutorId = request.data.get("id")

        payobj = CoursePayment.objects.filter(tutorId_id=tutorId)
        print(payobj.values(),"#########3")

        serialized = CoursePaymentSerializer(payobj,many=True)

        return Response({"paydata":serialized.data})
    
class NotesDataView(APIView):
    def post(self,request):
        id = request.data.get("id")
        stdobj = Student.objects.get(id=id)
        notesobj = MyNotes.objects.filter(student_id=stdobj)
        print(notesobj.values(),">>>>")
        serialized = MyNotesSerializer(notesobj,many=True)

        return Response(serialized.data)
    
class GetNotesDataView(APIView):
    def post(self,request):
        id = request.data.get("id")
        # stdobj = Student.objects.get(id=id)
        notesobj = MyNotes.objects.get(id=id)
        # print(notesobj.values(),">>>>")
        serialized = MyNotesSerializer(notesobj)

        return Response(serialized.data)
    
class AddNotesView(APIView):
    def post(self,request):
        notes = request.data.get("notes")
        id = request.data.get("id")

        if notes.isspace():
            return Response({"message": "Invalid Data in Notes (contains only spaces)"})

        notesobj = MyNotes.objects.create(student_id=id,notes=notes)
        serialized = MyNotesSerializer(notesobj)

        return Response({"message":"success","data":serialized.data})
    
class EditNotesView(APIView):
    def post(self,request):
        id = request.data.get("id")
        notes = request.data.get("notes")      

        notesobj = MyNotes.objects.get(id=id)
        notesobj.notes=notes
        notesobj.save()

        notesobj = MyNotes.objects.get(id=id)
        serialized = MyNotesSerializer(notesobj)

        return Response(serialized.data)
    
class DeleteNotesView(APIView):
    def post(self,request):
        id = request.data.get("id")     

        notesobj = MyNotes.objects.get(id=id)
        notesobj.delete()

        return Response({"message":"deleted"})
    
class StatusBlockview(APIView):
    def post(self,request):
        id = request.data.get("id")
        stdobj = Student.objects.get(id=id)
        curr_status = stdobj.status
        
        if curr_status == False:
            stdobj.status = True
        # else:
        #     stdobj.status = True

        print(stdobj.status,"$$$$$$$$$",stdobj.name)
        stdobj.save()

        serialized = StudentSerializer(stdobj)

        return Response({"message":"status-block updated","data":serialized.data})
    
class StatusUnblockview(APIView):
    def post(self,request):
        id = request.data.get("id")
        stdobj = Student.objects.get(id=id)
        curr_status = stdobj.status
        
        if curr_status == True:
            stdobj.status = False
        # else:
        #     stdobj.status = True

        print(stdobj.status,"$$$$$$$$$",stdobj.name)
        stdobj.save()

        serialized = StudentSerializer(stdobj)

        return Response({"message":"status-unblock updated","data":serialized.data})
    
def generate_link():
    characters = string.ascii_letters + string.digits
    link=""
    for i in range(8):
        link+=random.choice(characters)

    return link 
    
class SessionAssignView(APIView):
    def post(self,request):
        date_time = request.data.get("date_time")
        notes = request.data.get("notes")
        student = request.data.get("student")
        tutor = request.data.get("tutor")
        course_struct = request.data.get("course_struct")

        linkobj = generate_link()
        video_link = linkobj

        print(date_time,"\n",notes,"\n",student,"\n",tutor,"\n",course_struct,"\n",linkobj,"@@@@@@@@@")

        session_obj = SessionAssign.objects.create(date_time=date_time,notes=notes,student_id=student,tutor_id=tutor,course_struct_id=course_struct,video_link=video_link)
        serialized = SessionAssignSerializer(session_obj)

        return Response(serialized.data)
    

class SessionDetailsView(APIView):
    def post(self,request):
        id = request.data.get("id")
        print(id,"###")

        details = SessionAssign.objects.filter(tutor_id=id)
        serialized = SessionAssignSerializer(details,many=True)

        return Response(serialized.data)
        
class SessionSendMailView(APIView):
    def post(self,request):
        roomId = request.data.get("roomId")

        sessionobj = SessionAssign.objects.get(video_link=roomId)
        emailobj = sessionobj.student.email

        subject = "Session Link"
        message = f"http://localhost:3000/zego?roomID={sessionobj.video_link}"
        recipient = emailobj
        send_mail(subject, 
            message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        
        return Response({"message":"success"})


class AddActivityTaskView(APIView):
    def post(self,request):
        std = request.data.get("studentId")
        tutor = request.data.get("tutorId")
        struct = request.data.get("coursePlan")
        task = request.data.get("task")

        structobj = CourseStructure.objects.get(title=struct)
        stdobj = Student.objects.get(id=std)
        tutorobj = Tutor.objects.get(id=tutor)
        print(structobj,"\n",tutorobj,"\n",stdobj,"\n")

        try:
            sessionobj = SessionAssign.objects.get(student=stdobj,tutor=tutorobj,course_struct=structobj)

            ActivityAssign.objects.create(task=task,session_assign=sessionobj)

        except:
            return Response({"message":"no sessions found"})
      

        return Response({"message":"Task added"})
    
class TaskDetailsView(APIView):
    def post(self,request):
        student = request.data.get("id")
        print(student,"&&&")
        sessionobj = SessionAssign.objects.get(student=student)
        taskobj = ActivityAssign.objects.filter(session_assign=sessionobj)
        print(sessionobj,"******",taskobj)

        taskCount = taskobj.count()

        completed_tasks = taskobj.filter(status="Completed")
        completedCount = completed_tasks.count()

        pending_tasks = taskobj.filter( Q(status="Task Assigned") | Q(status="Pending"))
        pendingCount = pending_tasks.count()

        serialized = ActivityAssignSerializer(taskobj,many=True)
        task_serialized = ActivityAssignSerializer(completed_tasks,many=True)
        pending_serialized = ActivityAssignSerializer(pending_tasks,many=True)

        return Response({"message":"hi data of tasks","data":serialized.data,"taskCount":taskCount,"completed_tasks":task_serialized.data,"completedCount":completedCount,'pendingTasks':pending_serialized.data,'pendingCount':pendingCount})
    
class ActivityDetailsView(APIView):
    def post(self,request):
        id = request.data.get("id")

        activityobj = ActivityAssign.objects.get(id=id)
        serialized = ActivityAssignSerializer(activityobj)

        return Response(serialized.data)
    
class TaskUploadView(APIView):
    def post(self,request):
        file = request.data.get("video")
        student = request.data.get("student")
        task = request.data.get("task")

        taskobj = ActivityAssign.objects.get(id=task)

        if file.content_type.split('/')[0] != 'video':
            return Response({'error': 'File must be a video'})

        # Create a Video_upload instance with the Cloudinary URL
        result = upload(file, resource_type="video",folder="DanceAcademy/task-uploads")

        task_upload = TaskUpload(
            task_upload=result['secure_url'],  # Store the Cloudinary URL
            up_time=timezone.now(),
            description=request.data.get('description', '') ,
            task=taskobj
        )
        
        task_upload.save()
        task_upload.student.add(student)

        taskobj.status="Completed"
        taskobj.save()

        print(task_upload,"&&&&&&&&&&*********")

        return Response({'url': task_upload.task_upload,'message':"success"})
    
class CourseStructDetailsView(APIView):
    def post(self,request):
        id = request.data.get('id')

        details = CoursePayment.objects.filter(studentId_id=id)

        serialized = CoursePaymentSerializer(details,many=True)
        return Response(serialized.data)
    

class CoursePayDetailsView(APIView):
    def post(self,request):
        totalAmount = 0
        stdId = request.data.get("id")

        payobj = CoursePayment.objects.filter(studentId_id=stdId)
        print(payobj.values(),"#########3")
        
        for i in payobj:
            totalAmount+= i.structId.price

        serialized = CoursePaymentSerializer(payobj,many=True)

        return Response({"paydata":serialized.data,"totalAmount":totalAmount})