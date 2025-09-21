from django.urls import path
# import views
from . import views
#app_name
app_name = 'contact'

urlpatterns = [
    path('en/contact/',views.contact,name='contact'),
    
    #================================AR============================================
    path('ar/contact/',views.contact_ar,name='contact_ar'),

]
