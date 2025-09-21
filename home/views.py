from django.shortcuts import render ,redirect
# import login_required
from django.contrib.auth.decorators import login_required
from users.models import CustomUser

# Create your views here.
#import profile from accounts
from accounts.models import Profile


from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

#home
@login_required
def home(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    
    
    
    
    context={
        'profile':user_profile,
    }
    return render(request,'home.html',context)


#=====================================AR==========================================

def home_ar(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    
    
    
    
    context={
        'profile':user_profile,
    }
    return render(request,'ar/home.html',context)



def send_emails(request):
    if request.method == 'POST':
        # Get the form data
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_ids = request.POST.getlist('recipients')  # list of selected user IDs

        # Fetch the selected users
        recipients = CustomUser.objects.filter(id__in=recipient_ids)

        # Extract email addresses
        recipient_emails = [user.email for user in recipients]

        # Send emails
        if recipient_emails:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Sender email
                recipient_emails,  # List of recipients
                fail_silently=False,
            )
            messages.success(request, f"Emails sent to {len(recipient_emails)} users.")
        else:
            messages.warning(request, "No users selected.")
        
    # If GET request, display the form
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'emails.html', context)



def send_emails_ar(request):
    if request.method == 'POST':
        # Get the form data
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_ids = request.POST.getlist('recipients')  # list of selected user IDs

        # Fetch the selected users
        recipients = CustomUser.objects.filter(id__in=recipient_ids)

        # Extract email addresses
        recipient_emails = [user.email for user in recipients]

        # Send emails
        if recipient_emails:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Sender email
                recipient_emails,  # List of recipients
                fail_silently=False,
            )
            messages.success(request, f"تم ارسال الرسالة الي {len(recipient_emails)} مشترك .")
        else:
            messages.warning(request, "ليس هناك مستخدمين مختارين.")
        
    # If GET request, display the form
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'ar/emails.html', context)




#error_404_view
@login_required
def error_404_view(request,exception):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    
    
    
    
    context={
        'profile':user_profile,
    }
    return render(request,'404.html',context)


@login_required
def error_500_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    
    
    
    
    context={
        'profile':user_profile,
    }
    return render(request,'404.html',context)




