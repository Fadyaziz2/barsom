from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from accounts.utils import get_profile_or_missing_response
from moviepy.editor import VideoFileClip

from .models import Course, Lecture, ViewLecture, ViewCourse

# Create your views here.

# #courses_category
@login_required
def courses_category(request):
    user_profile, missing_response = get_profile_or_missing_response(request, language="en")
    if missing_response:
        return missing_response

    user = request.user
    if getattr(user_profile, "is_placeholder", False) or user.has_right_sign:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(member_ship__lte=user_profile.membership)

    for course in courses:
        course.lectures_count = course.lecture_set.count()
        course.is_viewed = ViewCourse.objects.filter(user=user, course=course).exists()

    context = {
        "profile": user_profile,
        "courses": courses,
    }
    return render(request, "courses.html", context)





#courses_lect
@login_required
def courses_lect(request,id):
    user_profile, missing_response = get_profile_or_missing_response(request, language="en")
    if missing_response:
        return missing_response

    user = request.user
    lectures = Lecture.objects.filter(course=id).order_by("number")

    for lecture in lectures:
        video = VideoFileClip(lecture.video.path)
        duration_minutes = round(video.duration / 60, 1)
        lecture.duration = f"{duration_minutes} min"
        lecture.is_viewed = ViewLecture.objects.filter(user=user, lecture=lecture).exists()

    context = {
        "profile": user_profile,
        "lectures": lectures,
    }
    return render(request, "course-lect.html", context)

#course_details
@login_required
def course_details(request,id):
    user_profile, missing_response = get_profile_or_missing_response(request, language="en")
    if missing_response:
        return missing_response

    lecture = Lecture.objects.get(id=id)

    context = {
        "profile": user_profile,
        "lecture": lecture,
    }
    return render(request, "course-details.html", context)








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
    user_profile, missing_response = get_profile_or_missing_response(request, language="ar")
    if missing_response:
        return missing_response

    user = request.user
    if getattr(user_profile, "is_placeholder", False) or user.has_right_sign:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(member_ship__lte=user_profile.membership)

    for course in courses:
        course.lectures_count = course.lecture_set.count()
        course.is_viewed = ViewCourse.objects.filter(user=user, course=course).exists()

    context = {
        "profile": user_profile,
        "courses": courses,
    }
    return render(request, "ar/courses.html", context)

#courses_lect
@login_required
def courses_lect_ar(request,id):
    user_profile, missing_response = get_profile_or_missing_response(request, language="ar")
    if missing_response:
        return missing_response

    user = request.user
    lectures = Lecture.objects.filter(course=id).order_by("number")

    for lecture in lectures:
        video = VideoFileClip(lecture.video.path)
        duration_minutes = round(video.duration / 60, 1)
        lecture.duration = f"{duration_minutes} دقيقة"
        lecture.is_viewed = ViewLecture.objects.filter(user=user, lecture=lecture).exists()

    context = {
        "profile": user_profile,
        "lectures": lectures,
    }
    return render(request, "ar/course-lect.html", context)




#course_details
@login_required
def course_details_ar(request,id):
    user_profile, missing_response = get_profile_or_missing_response(request, language="ar")
    if missing_response:
        return missing_response

    lecture = Lecture.objects.get(id=id)

    context = {
        "profile": user_profile,
        "lecture": lecture,
    }
    return render(request, "ar/course-details.html", context)



