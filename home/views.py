from django.shortcuts import render, redirect
# import login_required
from django.contrib.auth.decorators import login_required
from users.models import CustomUser

# Create your views here.
#import profile from accounts
from accounts.utils import get_profile_or_missing_response


from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

#home
@login_required
def home(request):
    user_profile, missing_response = get_profile_or_missing_response(request, language="en")
    if missing_response:
        return missing_response

    context={
        'profile':user_profile,
    }
    return render(request,'home.html',context)


#=====================================AR==========================================

@login_required
def home_ar(request):
    user_profile, missing_response = get_profile_or_missing_response(request, language="ar")
    if missing_response:
        return missing_response

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
    language = "ar" if request.path.startswith("/ar/") else "en"
    user_profile, missing_response = get_profile_or_missing_response(request, language=language)
    if missing_response:
        return missing_response

    template_name = 'ar/404.html' if language == 'ar' else '404.html'

    context={
        'profile':user_profile,
    }
    return render(request, template_name, context, status=404)


@login_required
def error_500_view(request):
    language = "ar" if request.path.startswith("/ar/") else "en"
    user_profile, missing_response = get_profile_or_missing_response(request, language=language)
    if missing_response:
        return missing_response

    template_name = 'ar/404.html' if language == 'ar' else '404.html'

    context={
        'profile':user_profile,
    }
    return render(request, template_name, context, status=500)




