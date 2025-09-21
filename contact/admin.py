from django.contrib import admin
#import Contact
from .models import Contact
# Register your models here.

#search
class ContactAdmin(admin.ModelAdmin):
    search_fields = ['name','email','subject','message']
    class Meta:
        model = Contact
        
admin.site.register(Contact,ContactAdmin)
