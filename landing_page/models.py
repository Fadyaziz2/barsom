from django.db import models
from users.models import CustomUser
from ckeditor.fields import RichTextField
# Create your models here.

class UserLandingPage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True,blank=True)
    title_ar=models.CharField(max_length=100,verbose_name="Arabic title",null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    description_ar = models.TextField(verbose_name="Arabic description", null=True, blank=True)
    image = models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    video = models.FileField(upload_to='static/landing_page/video', null=True, blank=True)
    pagename = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)




class MainSection(models.Model):
    title=models.CharField(max_length=100)
    title_ar=models.CharField(max_length=100,verbose_name="Arabic title")
    
    description=models.TextField()
    description_ar=models.TextField(verbose_name="Arabic Description")
    image=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    
    def __str__(self):
        return str(self.title)
    
    
    
class SocialMedia(models.Model):
    icon=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    name=models.CharField(max_length=100)
    link=models.URLField()
    
    def __str__(self):
        return str(self.name)


    
class CoursesSection(models.Model):
    title=models.CharField(max_length=100)
    title_ar=models.CharField(max_length=100,verbose_name="Arabic title")
    description=models.TextField()
    description_ar=models.TextField(verbose_name="Arabic Description")
    image=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    video=models.FileField(upload_to='static/landing_page/video', null=True, blank=True)
    video_poster=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    def __str__(self):
        return str(self.title)
    
    
class BenfitsSection(models.Model):
    title=models.CharField(max_length=100)
    title_ar=models.CharField(max_length=100,verbose_name="Arabic title")
    description=models.TextField()
    description_ar=models.TextField(verbose_name="Arabic Description")
    
    
    def __str__(self):
        return str(self.title)
    
    
class Pricing(models.Model):
    name=models.CharField(max_length=100,verbose_name="Name")
    name_ar=models.CharField(max_length=100,verbose_name="Arabic name")
    image=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)
    
    features=models.TextField(verbose_name="opinions")
    features_ar=models.TextField(verbose_name="Arabic opinions")
    
    video=models.FileField(upload_to='static/landing_page/video', null=True, blank=True)
    video_poster=models.ImageField(upload_to='static/landing_page/image', null=True, blank=True)

    terabox_url=models.URLField(verbose_name="Terabox URL", null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    
    class Meta:
        verbose_name_plural = "Users' opinions"
        verbose_name = "User's opinion"
    
    
class MainLandingPage(models.Model):
    # One-to-Many relationship with MainSection
    main_section = models.ForeignKey(MainSection, on_delete=models.CASCADE, related_name='landing_pages')
    # Many-to-Many relationships
    courses_sections = models.ManyToManyField(CoursesSection, related_name='landing_pages')
    benefits_sections = models.ManyToManyField(BenfitsSection, related_name='landing_pages')
    benfits_image=models.ImageField(upload_to="static/landing_page/image",null=True,blank=True)
    social_medias = models.ManyToManyField(SocialMedia, related_name='landing_pages')
    pricing_plans = models.ManyToManyField(Pricing, related_name='landing_pages' , verbose_name='Users opinions')
    
    def __str__(self):
        return f"Landing Page {self.id}"
    
 
 
class Video_message(models.Model):
    message=models.CharField(max_length=100)
    message_ar=models.CharField(max_length=100,verbose_name="Arabic message")

    def __str__(self):
        return str(self.message)
 
    
    
class UserRequested(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    notes=models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    
    conected=models.BooleanField(default=False,null=True,blank=True)
    mynotes=models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return str(self.name)
    
    
    
