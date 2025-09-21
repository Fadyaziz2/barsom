from django.db import models
from courses.models import Course
from ckeditor.fields import RichTextField
# Create your models here.

class wellcome_message(models.Model):
    message=RichTextField(verbose_name="English message")
    message_ar=RichTextField(verbose_name="Arabic message")

    def __str__(self):
        return self.message
    
    
class reset_password_message(models.Model):
    message=RichTextField( verbose_name="English message")
    message_ar=RichTextField( verbose_name="Arabic message")

    def __str__(self):
        return self.message
    
    
class CourseMessage(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    message=RichTextField(verbose_name="English message")
    message_ar=RichTextField(verbose_name="Arabic message")

    def __str__(self):
        return self.message
    

    