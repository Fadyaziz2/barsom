from django.urls import path
# import views
from . import views
#app_name
app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('en/home',views.home,name='home'),
    path('ar/home',views.home_ar,name='home_ar'),
    path('en/send_emails',views.send_emails,name='send_emails'),
    path('ar/send_emails',views.send_emails_ar,name='send_emails_ar'),
]

