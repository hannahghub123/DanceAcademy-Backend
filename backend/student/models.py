from django.db import models
from tutor.models import *

# Create your models here.
 
class Student(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default=None)
    phone = models.PositiveIntegerField()
    password = models.CharField(max_length=50, default=None)
    score = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="student-images",null=True,blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True,default=1)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}-{self.id}"
    
class CoursePayment(models.Model):
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    structId = models.ForeignKey(CourseStructure, on_delete=models.CASCADE)
    tutorId = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    razorpayId = models.CharField( max_length=250)

class MyNotes(models.Model):
    notes = models.CharField(max_length=1000,default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Notes - {self.student.name}"
    
class SessionAssign(models.Model):
    date_time = models.DateTimeField()
    video_link = models.CharField(max_length=200,default="video-link")
    notes = models.CharField(max_length=500,null=True,blank=True,default="Session Assigned")
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course_struct = models.ForeignKey(CourseStructure,on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.tutor.name}-{self.student.name}-{self.course_struct.title}"

class ActivityAssign(models.Model):
    STATUS_CHOICES=(
        ("Completed","Completed"),
        ("Pending","Pending"),
        ("Done Late","Done Late"),
        ("Task Assigned","Task Assigned")
    )
    task = models.CharField(max_length=1000)
    session_assign = models.ForeignKey(SessionAssign, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="Task Assigned")
    # time_added = models.DateTimeField()

    def __str__(self):
        return f"{self.session_assign.tutor}-{self.session_assign.student.name}/{self.session_assign.course_struct.course}-{self.session_assign.course_struct.title}"
    

class TaskUpload(models.Model):
    task_upload = CloudinaryField("Task uploads",max_length=1000,null=True,blank=True,  folder='DanceAcademy/task-uploads')
    up_time = models.DateTimeField()
    description = models.CharField(max_length=220)
    student = models.ManyToManyField(Student, related_name='tasks', blank=True)
    task = models.ForeignKey(ActivityAssign,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Video Upload {self.id}"