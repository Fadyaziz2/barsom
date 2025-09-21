from django.shortcuts import render
from .models import MainLandingPage , UserLandingPage , UserRequested , Video_message
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
# import messages
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.

def LandingPage(request):
    # get first landing page
    landing_page = MainLandingPage.objects.first()
    if request.method=='POST':
        name=request.POST.get('name', '').strip()
        email=request.POST.get('email', '').strip()
        phone=request.POST.get('phone', '').strip()
        age=request.POST.get('age', '').strip()
        gender=request.POST.get('gender', '').strip()
        location=request.POST.get('location', '').strip()
        notes=request.POST.get('notes', '').strip()
        
        user_landing_page=UserRequested.objects.create(name=name,email=email,phone=phone,age=age,gender=gender,location=location,notes=notes)    
        user_landing_page.save()
        messages.success(request, 'your request has been sent successfully')
    
    
    
    
    context = {
        'landing_page':landing_page
    }
    return render(request,'landing_page.html',context)

@login_required
def UserLandingPagedef(request):
    user = request.user
    user_landing_page = UserLandingPage.objects.filter(user=user).first()
    requested = UserRequested.objects.filter(user=user)
    
    if request.method=='POST':
        image=request.FILES.get('image')
        video=request.FILES.get('video')
        title=request.POST.get('title')
        title_ar=request.POST.get('title_ar')
        description=request.POST.get('description')
        description_ar=request.POST.get('description_ar')
        
        # get name for user from his profile 
        user_profile = Profile.objects.get(user=user)
        print("pagename=" , user_profile.name)
        
        if user_landing_page:
            user_landing_page.image=image
            user_landing_page.video=video
            user_landing_page.title=title
            user_landing_page.title_ar=title_ar
            user_landing_page.description=description
            user_landing_page.description_ar=description_ar
            user_landing_page.pagename=user_profile.name
            user_landing_page.save()
            messages.success(request, 'your profile has been updated successfully')
        else:
            user_landing_page = UserLandingPage.objects.create(user=user)
            user_landing_page.image=image
            user_landing_page.video=video
            user_landing_page.title=title
            user_landing_page.title_ar=title_ar
            user_landing_page.description=description
            user_landing_page.description_ar=description_ar
            user_landing_page.pagename=user_profile.name
            user_landing_page.save()
            messages.success(request, 'your profile has been created successfully')
    context = {
        'user_landing_page':user_landing_page,
        'requested':requested,
    }
    return render(request,'inneruserlandingpage.html',context)


def outuserlandingpage(request,pagename):
    video=Video_message.objects.first()
        
    page=UserLandingPage.objects.get(pagename=pagename)
    context={
        'landing_page':page,
        'video':video
    }
    if request.method=='POST':
        name=request.POST.get('name', '').strip()
        email=request.POST.get('email', '').strip()
        phone=request.POST.get('phone', '').strip()
        age=request.POST.get('age', '').strip()
        gender=request.POST.get('gender', '').strip()
        location=request.POST.get('location', '').strip()
        notes=request.POST.get('notes', '').strip()
        #user = CustomUser that create this landing page
        user = page.user
        user_landing_page=UserRequested.objects.create(name=name,email=email,phone=phone,age=age,gender=gender,location=location,notes=notes,user=user)    
        user_landing_page.save()
        messages.success(request, 'your request has been sent successfully')
        return redirect('landing_page:LandingPage')
        
    return render(request,'userlandingpage.html',context)




#-------------------------ar --------------------------


def LandingPage_ar(request):
    
    # get first landing page
    landing_page = MainLandingPage.objects.first()
    if request.method=='POST':
        name=request.POST.get('name', '').strip()
        email=request.POST.get('email', '').strip()
        phone=request.POST.get('phone', '').strip()
        age=request.POST.get('age', '').strip()
        gender=request.POST.get('gender', '').strip()
        location=request.POST.get('location', '').strip()
        notes=request.POST.get('notes', '').strip()
        user_landing_page=UserRequested.objects.create(name=name,email=email,phone=phone,age=age,gender=gender,location=location,notes=notes)    
        user_landing_page.save()
        messages.success(request, 'your request has been sent successfully')
    
    context = {
        'landing_page':landing_page
    }
    return render(request,'ar/landing_page.html',context)

@login_required
def UserLandingPagedef_ar(request):
    user = request.user
    user_landing_page = UserLandingPage.objects.filter(user=user).first()
    requested = UserRequested.objects.filter(user=user)
    
    if request.method=='POST':
        image=request.FILES.get('image')
        video=request.FILES.get('video')
        title=request.POST.get('title')
        title_ar=request.POST.get('title_ar')
        description=request.POST.get('description')
        description_ar=request.POST.get('description_ar')
        
        # get name for user from his profile 
        user_profile = Profile.objects.get(user=user)
        print("pagename=" , user_profile.name)
        
        if user_landing_page:
            user_landing_page.image=image
            user_landing_page.video=video
            user_landing_page.title=title
            user_landing_page.title_ar=title_ar
            user_landing_page.description=description
            user_landing_page.description_ar=description_ar
            user_landing_page.pagename=user_profile.name
            user_landing_page.save()
            messages.success(request, 'your profile has been updated successfully')
        else:
            user_landing_page = UserLandingPage.objects.create(user=user)
            user_landing_page.image=image
            user_landing_page.video=video
            user_landing_page.title=title
            user_landing_page.title_ar=title_ar
            user_landing_page.description=description
            user_landing_page.description_ar=description_ar
            user_landing_page.pagename=user_profile.name
            user_landing_page.save()
            messages.success(request, 'your profile has been created successfully')
    context = {
        'user_landing_page':user_landing_page,
        'requested':requested,
    }
    return render(request,'ar/inneruserlandingpage.html',context)


def outuserlandingpage_ar(request,pagename):
    video=Video_message.objects.first()
    page=UserLandingPage.objects.get(pagename=pagename)
    context={
        'landing_page':page,
        'video':video
    }
    if request.method=='POST':
        name=request.POST.get('name', '').strip()
        email=request.POST.get('email', '').strip()
        phone=request.POST.get('phone', '').strip()
        age=request.POST.get('age', '').strip()
        gender=request.POST.get('gender', '').strip()
        location=request.POST.get('location', '').strip()
        notes=request.POST.get('notes', '').strip()
        #user = CustomUser that create this landing page
        user = page.user
        user_landing_page=UserRequested.objects.create(name=name,email=email,phone=phone,age=age,gender=gender,location=location,notes=notes,user=user)    
        user_landing_page.save()
        messages.success(request, 'your request has been sent successfully')
        return redirect('landing_page:LandingPage_ar')
    return render(request,'ar/userlandingpage.html',context)






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserRequested

@csrf_exempt
def update_requests(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.POST.get('requests'))

            # Iterate through the data and update the corresponding records
            for item in data:
                user_request = UserRequested.objects.get(id=item['id'])
                user_request.conected = item['conected']
                user_request.mynotes = item['mynotes']
                user_request.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
