from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from accounts.utils import get_profile_or_missing_response
import logging

from moviepy.editor import VideoFileClip

from .models import Course, Lecture, ViewLecture, ViewCourse


logger = logging.getLogger(__name__)


def _get_video_duration_minutes(video_field):
    """Return the video duration in minutes or ``None`` on failure."""
    try:
        with VideoFileClip(video_field.path) as clip:
            return clip.duration / 60
    except Exception as exc:  # moviepy may raise different OSErrors depending on ffmpeg
        logger.warning("Failed to read duration for %s: %s", video_field.name, exc)
        return None


def _format_duration(minutes, language="en"):
    if minutes is None:
        return "Unknown" if language == "en" else "غير متاح"
    rounded = round(minutes, 1)
    if language == "ar":
        return f"{rounded} دقيقة"
    return f"{rounded} min"

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
        minutes = _get_video_duration_minutes(lecture.video)
        lecture.duration = _format_duration(minutes, language="en")
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








@login_required
def view_lect(request, lect_id):
    try:
        lecture = Lecture.objects.select_related("course").get(id=lect_id)
        course = lecture.course
        user = request.user

        ViewLecture.objects.update_or_create(
            user=user,
            lecture=lecture,
            defaults={"time": 0},
        )

        next_lecture = (
            Lecture.objects.filter(course=course, number__gt=lecture.number)
            .order_by("number")
            .first()
        )

        if next_lecture:
            ViewLecture.objects.get_or_create(
                user=user,
                lecture=next_lecture,
                defaults={"time": 0},
            )
        else:
            next_course = (
                Course.objects.filter(number__gt=course.number)
                .order_by("number")
                .first()
            )
            if next_course:
                ViewCourse.objects.get_or_create(
                    user=user,
                    course=next_course,
                    defaults={"time": 0},
                )

        return HttpResponse("done")
    except Lecture.DoesNotExist:
        return HttpResponse("Lecture not found", status=404)
    except Exception as exc:
        logger.exception("Failed to update lecture progress for user %s", request.user)
        return HttpResponse(str(exc), status=500)
    
                
                





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
        minutes = _get_video_duration_minutes(lecture.video)
        lecture.duration = _format_duration(minutes, language="ar")
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



