from django.contrib import admin
#import courses lecture
from .models import Lecture , Course ,ViewLecture
# Register your models here.


def remove_duplicate_view_lectures(modeladmin, request, queryset):
    unique_records = []
    duplicate_records = []
    
    for record in queryset:
        # Create a unique identifier based on user and lecture
        identifier = (record.user, record.lecture)
        
        if identifier not in unique_records:
            unique_records.append(identifier)
        else:
            duplicate_records.append(record)
    
    # Delete duplicate records
    for duplicate_record in duplicate_records:
        duplicate_record.delete()

    modeladmin.message_user(
        request,
        f"{len(duplicate_records)} duplicate ViewLecture records removed.",
    )

remove_duplicate_view_lectures.short_description = "Remove duplicate ViewLecture records"






#search
class LectureAdmin(admin.ModelAdmin):
    search_fields = ['title']
    class Meta:
        model = Lecture
        
#search
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['title']
    class Meta:
        model = Course

#view lecture display all fields    
class ViewLectureAdmin(admin.ModelAdmin):
    list_display = ['user','lecture','time','create_at']
    search_fields = ['user','course']
    class Meta:
        model = ViewLecture
        
    actions = [remove_duplicate_view_lectures]



admin.site.register(Lecture,LectureAdmin)
admin.site.register(Course,CourseAdmin)




admin.site.register(ViewLecture,ViewLectureAdmin)
