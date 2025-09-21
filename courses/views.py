from django.shortcuts import render
#import login_required
from django.contrib.auth.decorators import login_required
#import Profile from accounts
from accounts.models import Profile , MemberShip
#import course , lecture
from .models import Course , Lecture , Lecture_rate , ViewLecture , ViewCourse
#import redirct
from django.shortcuts import redirect
#import video file clip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from django.db.models import Sum
#import timezone
from django.utils import timezone
#import timedelta
from datetime import timedelta
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

# #courses_category
@login_required
def courses_category(request):
     user = request.user
     user_profile = Profile.objects.get(user=user)
     if user.has_right_sign:
         #get all course
          courses = Course.objects.all()
     else:
         #get course on user membership and courses that user membership less than course membership
         courses = Course.objects.filter(member_ship__lte=user_profile.membership) 
     #get number of all lecture in this course
     for course in courses:
         course.lectures_count = len(course.lecture_set.all())
     #add atrribute to course to check if this course is viewed by this user
     for course in courses:
         if ViewCourse.objects.filter(user=user,course=course).exists():
             course.is_viewed = True
         else:
             course.is_viewed = False
     context={
         'profile':user_profile,
         'courses':courses,
     }
     return render(request,'courses.html',context)





#courses_lect
@login_required
def courses_lect(request,id):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    #get lecture 
    lectures = Lecture.objects.filter(course=id).order_by('number')
    #get all lectures video duration
    for lecture in lectures:
        video = VideoFileClip(lecture.video.path)
        lecture.duration = video.duration
        lecture.duration = round(lecture.duration / 60,1)
        lecture.duration = str(lecture.duration) + ' min'
    
    #add atrribute to lecture to check if this lecture is viewed by this user
    for lecture in lectures:
        viewlectures = ViewLecture.objects.filter(user=user, lecture=lecture)
        if viewlectures.exists():
            lecture.is_viewed = True
        else:
            lecture.is_viewed = False

            

    context={
        'profile':user_profile,
        'lectures':lectures,
    }
    return render(request,'course-lect.html',context)

#course_details
@login_required
def course_details(request,id):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    #get lecture by id
    lecture = Lecture.objects.get(id=id)
     #get course for this lecture
    course = Course.objects.get(id=lecture.course.id)
    context={
        'profile':user_profile,
        'lecture':lecture,
    }
    return render(request,'course-details.html',context)








def view_lect(request,lect_id):
    try:
        
        user = request.user
        id=lect_id
        #get lecture by id
        lecture = Lecture.objects.get(id=id)
        #get course for this lecture
        course = Course.objects.get(id=lecture.course.id)
        #add  next lecture in ViewLecture if not exist
        next_lecture = Lecture.objects.filter(course=course,number=lecture.number+1)
        #check if next lecture exist
        if next_lecture.exists():
            #create new ViewLecture
            #check if this lecture is not viewed
            if not ViewLecture.objects.filter(user=user,lecture=next_lecture[0]).exists():
                ViewLecture.objects.create(user=user,lecture=next_lecture[0],time=0)
                print('next create')
        #get last lecture in this course
        last_lecture = Lecture.objects.filter(course=course).last()
        #check if last lecture exist in viewlecture
        if ViewLecture.objects.filter(user=user,lecture=last_lecture).exists():
            #add next course in ViewCourse if not exist
            #get next course
            next_course = Course.objects.filter(number=course.number+1)
            #check if next course exist
            if next_course.exists():
                #create new ViewCourse if not exist
                if not ViewCourse.objects.filter(user=user,course=next_course[0]).exists():
                    ViewCourse.objects.create(user=user,course=next_course[0],time=0)
                    print('last create')
        return HttpResponse('done')
    except Exception as e:
        return HttpResponse(e)
    
                
                





#=======================================AR========================================

#courses_category
@login_required
def courses_category_ar(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    
    if user.has_right_sign:
        #get all course
         courses = Course.objects.all()
    else:
        #get course on user membership
        courses = Course.objects.filter(member_ship__lte=user_profile.membership)     
    #get number of all lecture in this course
    for course in courses:
        course.lectures_count = len(course.lecture_set.all())
    
    
    #set fully_star and empty_star in course depend on course.rate
    # for course in courses:
    #     course.fully_star = range(course.rate)
    #     course.empty_star = range(5-course.rate)
        
    
    #add atrribute to course to check if this course is viewed by this user
    for course in courses:
        if ViewCourse.objects.filter(user=user,course=course).exists():
            course.is_viewed = True
        else:
            course.is_viewed = False

    context={
        'profile':user_profile,
        'courses':courses,
    }
    return render(request,'ar/courses.html',context)

#courses_lect
@login_required
def courses_lect_ar(request,id):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    #get lecture 
    lectures = Lecture.objects.filter(course=id).order_by('number')
    #get all lectures video duration
    for lecture in lectures:
        video = VideoFileClip(lecture.video.path)
        lecture.duration = video.duration
        lecture.duration = round(lecture.duration / 60,1)
        lecture.duration = str(lecture.duration) + ' دقيقة'
    
    
    #set fully_star and empty_star in lecture depend on lecture.Lecture_rate
    # for lecture in lectures:
    #     lecture.fully_star = range(lecture.rate)
    #     lecture.empty_star = range(5-lecture.rate)

     #add atrribute to lecture to check if this lecture is viewed by this user
    for lecture in lectures:
        viewlectures = ViewLecture.objects.filter(user=user, lecture=lecture)
        if viewlectures.exists():
            lecture.is_viewed = True
            
                        
                    
                
        else:
            lecture.is_viewed = False
    
    
    context={
        'profile':user_profile,
        'lectures':lectures,
    }
    return render(request,'ar/course-lect.html',context)




#course_details
@login_required
def course_details_ar(request,id):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    #get lecture by id
    lecture = Lecture.objects.get(id=id)
     #get course for this lecture
    course = Course.objects.get(id=lecture.course.id)
          
        

    context={
        'profile':user_profile,
        'lecture':lecture,
    }
    return render(request,'ar/course-details.html',context)



