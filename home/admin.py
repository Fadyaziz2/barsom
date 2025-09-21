from django.contrib import admin
from .models import wellcome_message , reset_password_message , CourseMessage
# Register your models here. 

admin.site.register(wellcome_message)
admin.site.register(reset_password_message)
admin.site.register(CourseMessage)