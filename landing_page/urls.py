from . import views
from django.urls import path

app_name = 'landing_page'
urlpatterns = [
    path('', views.LandingPage, name='LandingPage'),
    path('update_requests/', views.update_requests, name='update_requests'),
    path('userlandingpage/', views.UserLandingPagedef, name='UserLandingPage'),
    path('page/<str:pagename>', views.outuserlandingpage, name='outuserlandingpage'),
    
    #-----------------ar-----------------------
    path('ar/', views.LandingPage_ar, name='LandingPage_ar'),
    path('ar/userlandingpage', views.UserLandingPagedef_ar, name='UserLandingPage_ar'),
    path('page/ar/<str:pagename>', views.outuserlandingpage_ar, name='outuserlandingpage_ar'),
    
    
    
]