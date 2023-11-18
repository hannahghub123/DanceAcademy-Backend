from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.

class Course(models.Model):
    COURSE_STATUS_CHOICES = (
        ("Course Available","Course Available"),
        ("Seats Filled","Seats Filled")
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50,choices=COURSE_STATUS_CHOICES,default="Course Available")
    image = models.ImageField(upload_to="course-uploads", max_length=500,null=True,blank=True)

    def __str__(self):
        return f"{self.title}"

class CourseStructure(models.Model):
    LEVEL_CHOICES = (
        ("Beginner Level Lessons","Beginner Level Lessons"),
        ("Intermediate Level Lessons","Intermediate Level Lessons")
    )
    PRICE_CHOICES = (
        ("Month","Month"),
        ("Quarter","Quarter"),
        ("Year","Year"),
    )
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    num_of_classes = models.PositiveIntegerField()
    levels = models.CharField(max_length=50,choices=LEVEL_CHOICES,default="Beginner Level Lessons")
    price_per = models.CharField(max_length=50,choices=PRICE_CHOICES,default=None,null=True)

    def __str__(self):
        return f"{self.course.title}-{self.id}"


class Tutor(models.Model):
    STATUS_CHOICES=(
        ("Available","Available"),
        ("Not Available","Not Available")
    )
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    expertise = models.PositiveIntegerField(blank=True, null=True)
    email = models.CharField(max_length=50, default=None)
    phone = models.PositiveIntegerField()
    password = models.CharField(max_length=50, default=None)
    is_approved = models.BooleanField(default=False)
    course = models.ManyToManyField(Course)
    image = models.ImageField(upload_to="tutor-uploads", max_length=500,null=True,blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="Available")

    def __str__(self):
        return f"{self.name}"
    

class VideoUpload(models.Model):
    v_upload = CloudinaryField("Video uploads",max_length=500,null=True,blank=True,  folder='DanceAcademy/video-uploads')
    up_time = models.DateTimeField()
    desc = models.CharField(max_length=220)
    tutors = models.ManyToManyField(Tutor, related_name='videos', blank=True)

    def __str__(self):
        return f"Video Upload {self.id}"
    
class ResumeList(models.Model):
    res_file = CloudinaryField("Resume uploads",max_length=500,null=True,blank=True,  folder='DanceAcademy/resume-uploads')
    up_time = models.DateTimeField()
    tutors = models.ManyToManyField(Tutor, related_name='resume', blank=True)

    def __str__(self):
        return f"Resume Upload {self.id}"
    

