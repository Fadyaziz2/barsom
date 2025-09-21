from django.contrib import admin
#import membership
from .models import MemberShip,Profile,Rank
#search on membership,Profile
class MemberShipAdmin(admin.ModelAdmin):
    #search fields
    search_fields = ['name','price']

#Profile search
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name','address','birth_date','coin']
    #hidden field rank
    exclude = ('rank',)
    
class RankAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name','min_number']
    


#register
admin.site.register(MemberShip,MemberShipAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Rank,RankAdmin)
