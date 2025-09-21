
#import path
from django.urls import path

# import views
from . import views

#app_name
app_name = 'courses'

urlpatterns = [
    path('en/courses_category/',views.courses_category,name='courses_category'),
    path('en/courses_lect/<int:id>/',views.courses_lect,name='courses_lect'),
    path('en/course_details/<int:id>/',views.course_details,name='course_details'),
    #change_video_quality
    
    path('view_lect/<int:lect_id>/',views.view_lect,name='view_lect'),
    
    # url https://tradingwhaleschool.online/courses/view_lect/1
    #================================AR============================================
    
    path('ar/courses_category/',views.courses_category_ar,name='courses_category_ar'),
    path('ar/courses_lect/<int:id>/',views.courses_lect_ar,name='courses_lect_ar'),
    path('ar/course_details/<int:id>/',views.course_details_ar,name='course_details_ar'),
    
]
    