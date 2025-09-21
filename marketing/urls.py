
#import path
from django.urls import path

# import views
from . import views

#app_name
app_name = 'marketing'

urlpatterns = [
    path('en/marketing_courses_category/',views.marketing_courses_category,name='marketing_courses_category'),
    path('en/marketing_courses_lect/<int:id>/',views.marketing_courses_lect,name='marketing_courses_lect'),
    path('en/marketing_course_details/<int:id>/',views.marketing_course_details,name='marketing_course_details'),
 
    #================================AR============================================
    
    path('ar/marketing_courses_category/',views.marketing_courses_category_ar,name='marketing_courses_category_ar'),
    path('ar/marketing_courses_lect/<int:id>/',views.marketing_courses_lect_ar,name='marketing_courses_lect_ar'),
    path('ar/marketing_course_details/<int:id>/',views.marketing_course_details_ar,name='marketing_course_details_ar'),
    
]
    