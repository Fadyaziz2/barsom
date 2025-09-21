from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#get customuser,profile
from users.models import CustomUser
from accounts.models import Profile
#get contact
from .models import Contact
#import message
from django.contrib import messages
#import redirct
from django.shortcuts import redirect

# Create your views here.

#contact
@login_required
def contact(request):
    #send customuser , profile
    user = request.user
    my_profile = Profile.objects.get(user=user)
    #get custom user that create this user
    custom_user = CustomUser.objects.get(id=user.id)
    ended_at=custom_user.ended_at

    #get leader profile that create me
    if not user.is_superuser:
        created_by = Profile.objects.get(user=custom_user.create_by)
    else:
        created_by = my_profile
        
        
    #save send data
    if request.method == 'POST':
        #get data from form
        name = my_profile.name
        email = custom_user.email
        create_by = created_by.name
        ended_at = custom_user.ended_at
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        #save data
        contact = Contact(name=name,email=email,create_by=create_by,ended_at=ended_at,subject=subject,message=message)
        contact.save()
        #send message
        messages.success(request, 'your message has been sent successfully')
        #redirct to contact
        return redirect('contact:contact')
    
    #context
    context = {
        'profile':my_profile,
        'my_profile':my_profile,
        'custom_user':custom_user,
        'created_by':created_by,
        'ended_at':ended_at,
    }
    return render(request,'contact.html',context)





#=======================================AR========================================

@login_required
def contact_ar(request):
    #send customuser , profile
    user = request.user
    my_profile = Profile.objects.get(user=user)
    #get custom user that create this user
    custom_user = CustomUser.objects.get(id=user.id)
    ended_at=custom_user.ended_at

    #get leader profile that create me
    if not user.is_superuser:
        created_by = Profile.objects.get(user=custom_user.create_by)
    else:
        created_by = my_profile
        
        
    #save send data
    if request.method == 'POST':
        #get data from form
        name = my_profile.name
        email = custom_user.email
        create_by = created_by.name
        ended_at = custom_user.ended_at
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        #save data
        contact = Contact(name=name,email=email,create_by=create_by,ended_at=ended_at,subject=subject,message=message)
        contact.save()
        #send message
        messages.success(request, 'تم ارسال رسالتك بنجاح')
        #redirct to contact
        return redirect('contact:contact_ar')
    
    #context
    context = {
        'profile':my_profile,
        'my_profile':my_profile,
        'custom_user':custom_user,
        'created_by':created_by,
        'ended_at':ended_at,
    }
    return render(request,'ar/contact.html',context)
