from django.contrib import admin
from .models import UserLandingPage , MainSection , CoursesSection , BenfitsSection , Pricing , MainLandingPage, UserRequested,SocialMedia ,Video_message
# Register your models here.

admin.site.register(Pricing)
admin.site.register(MainLandingPage)
admin.site.register(UserRequested)
admin.site.register(Video_message)


admin.site.register(UserLandingPage)
admin.site.register(MainSection)
admin.site.register(CoursesSection)
admin.site.register(BenfitsSection)
admin.site.register(SocialMedia)