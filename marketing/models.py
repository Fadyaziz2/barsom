from django.db import models
from django.core.files.storage import FileSystemStorage
from moviepy.editor import VideoFileClip
#import MemberShip from accounts
from accounts.models import MemberShip
from users.models import CustomUser

# Create your models here.

#courses image title rate 
class Marketing_Course(models.Model):
    image = models.ImageField(upload_to='static/course/image')
    title = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['id']
    
    
    def __str__(self):
        return self.title
    
#course lecture title image description video url rate number duration
class Marketing_Lecture(models.Model):
    course = models.ForeignKey(Marketing_Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/course/image')
    description = models.TextField(null=True,blank=True)
    video = models.FileField(upload_to='static/course/video')
    number = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Marketing_Lecture_rate(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    lecture=models.ForeignKey(Marketing_Lecture,on_delete=models.CASCADE)
    star= models.IntegerField(default=0)

    
    
    


    

