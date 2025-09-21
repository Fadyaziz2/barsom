from django.contrib import admin
#import MemberShip, CustomUser
from .models import CustomUser
from django.core.mail import send_mail
#get email from setting
from django.conf import settings
from accounts.models import Profile
# Register your models here.

    
#search on customuser by name or email or phone 
class CustomUserAdmin(admin.ModelAdmin):
    #search fields
    search_fields = ['email','phone']
    #list display
    list_display = ['email','phone','is_staff','is_blocked']
    
    # action to delete users that not has profile 
    def delete_users_that_not_has_profile(self, request, queryset):
        for user in queryset:
            if not Profile.objects.filter(user=user).exists():
                user.delete()
    actions = [delete_users_that_not_has_profile]
    

    
    

admin.site.register(CustomUser,CustomUserAdmin)
