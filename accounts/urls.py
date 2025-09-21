# import path
from django.urls import path
# import views
from . import views

#app_name
app_name = 'accounts'

urlpatterns = [
    path('en/login/',views.log_in,name='login'),
    path('en/login/',views.log_in,name='login'),
    path('en/logout/',views.log_out,name='logout'),
    path('en/profile/',views.profile,name='profile'),
    path('en/add_new_member/',views.add_new_member,name='add_new_member'),
    path('en/send_coin/',views.send_coin,name='send_coin'),
    path('en/forget_pass/',views.forget_pass,name='forget_pass'),
    path('en/team_profile/<int:id>/',views.team_profile,name='team_profile'),
    path('en/reset-password/<int:id>/',views.reset_password,name='reset_password'),
    #upgrade_membership
    path('en/upgrade_membership/',views.upgrade_membership,name='upgrade_membership'),
    path('changeimage/',views.changeimage,name='changeimage'),
    
    #================================AR============================================
    path('login/',views.log_in_ar,name='login_ar'),
    path('ar/logout/',views.log_out_ar,name='logout_ar'),
    path('ar/profile/',views.profile_ar,name='profile_ar'),
    path('ar/add_new_member/',views.add_new_member_ar,name='add_new_member_ar'),
    path('ar/send_coin/',views.send_coin_ar,name='send_coin_ar'),
    path('ar/forget_pass/',views.forget_pass_ar,name='forget_pass_ar'),
    path('ar/team_profile/<int:id>/',views.team_profile_ar,name='team_profile_ar'),
    path('ar/reset-password/<int:id>/',views.reset_password_ar,name='reset_password_ar'),

    #upgrade_membership
    path('ar/upgrade_membership/',views.upgrade_membership_ar,name='upgrade_membership_ar'),
]
