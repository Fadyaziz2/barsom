# hello/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
#import Customuser
from users.models import CustomUser
#import timezone
from django.utils import timezone
#import timedelta
from datetime import timedelta
#import mail
from django.core.mail import send_mail
#import settings
from django.conf import settings



def Block_users():
    #block user that ended_at<now and not has right sign and create_at<create_at+duration
    blockeduser=CustomUser.objects.filter(ended_at__lt=timezone.now(),has_right_sign=False,isactive=True)
    for user in blockeduser:
        user.is_blocked=True
        user.save()
        #send mail to user
        send_mail(
            'Trading whale school',
            'your account is blocked',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
  

def active_users():
    #active users that create_at+duration<now
    activeuser=CustomUser.objects.filter(create_at__lt=timezone.now()-duration)
    
    for user in activeuser:
        user.isactive=True
        user.save()
        
    
    
    
    
def start_scheduler():
    scheduler = BackgroundScheduler()
    #every day
    scheduler.add_job(Block_users, 'interval', days=1)
    #every day
    scheduler.add_job(active_users, 'interval', days=1)
    scheduler.start()

