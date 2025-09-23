from django.shortcuts import render, get_object_or_404
#import login
from django.contrib.auth import authenticate, login,logout
# import login_required
from django.contrib.auth.decorators import login_required
#import redirct
from django.shortcuts import redirect
#import message
from django.contrib import messages
from django.db.models import Q
#import customsuer from users.models
from users.models import CustomUser
#import profile , membership from .models
from .models import Profile,MemberShip,Rank
#import timezone
from django.utils import timezone
#timedelta
from datetime import timedelta
#send mail
from django.core.mail import send_mail
#get email from setting
from django.conf import settings
#import os
import os
import random
import string 
from home.models import wellcome_message , reset_password_message

#imonport slugify
# Create your views here.


def random_string(length=6):
    """Generate a random string of letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def extend_membership_for_direct_partner(user, extension_days=30):
    """Extend ``user`` membership by ``extension_days`` after adding a direct partner."""

    if user.is_superuser:
        return

    now = timezone.now()
    current_end = user.ended_at
    base_date = current_end if current_end and current_end > now else now
    user.ended_at = base_date + timedelta(days=extension_days)
    user.save(update_fields=['ended_at'])


#log_in
def log_in(request):
    #login
    if request.method == 'POST':
        #get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticate user
        user = authenticate(request, username=username, password=password)
        access=False
        
        if user is not None:
            access=True
        else:
            #send message
            messages.error(request, 'the login data not correct')
            return render(request,'index.html')
    #check if user is blocked
        if user.is_blocked:
            #send message
            messages.error(request, 'Dear Trader, we would like to inform you that your educational period on the Whales Trading website has ended. If you wish to renew your subscription and continue your educational journey with us, please contact the responsible person to review the new plans. Thank you for choosing Whales Trading. We look forward to continuing to support you and providing you with the best educational experience. Best regards, The Whales Trading Team."')
            return render(request,'index.html')

        if user.ended_at and user.ended_at < timezone.now():
            messages.error(request, 'Your plan has ended. Please contact the administrators to renew your plan.')
            return render(request,'index.html')


        #if access = True login
        if access:
            login(request, user)
            #redirct to profile
            return redirect('home:home_ar')

    return render(request,'index.html')

#log_out
#login_required
@login_required
def log_out(request):
    logout(request)
    #redirct to login 
    return redirect('accounts:login')
    


    
    
    

# دالة لجمع كل الشركاء (المباشرين وغير المباشرين) لأي مستخدم
def get_partner_ids_by_status(user, reference_time=None):
    """Return two sets containing the IDs of active and ended partners for ``user``."""

    if reference_time is None:
        reference_time = timezone.now()

    current_level_ids = list(
        CustomUser.objects.filter(create_by=user).values_list('id', flat=True)
    )
    active_partner_ids = set()
    ended_partner_ids = set()
    processed_ids = set()

    while current_level_ids:
        partner_data = CustomUser.objects.filter(id__in=current_level_ids).values(
            'id', 'ended_at'
        )

        for data in partner_data:
            partner_id = data['id']
            ended_at = data['ended_at']
            if ended_at is None or ended_at >= reference_time:
                active_partner_ids.add(partner_id)
            else:
                ended_partner_ids.add(partner_id)

        processed_ids.update(current_level_ids)
        current_level_ids = list(
            CustomUser.objects.filter(create_by__in=current_level_ids)
            .exclude(id__in=processed_ids)
            .values_list('id', flat=True)
        )

    return active_partner_ids, ended_partner_ids


def calculate_partner_counts(user, reference_time=None):
    """Return the counts for direct, indirect, total active, and ended partners for ``user``."""

    if reference_time is None:
        reference_time = timezone.now()

    direct_partner_ids = set(
        CustomUser.objects.filter(create_by=user)
        .filter(Q(ended_at__isnull=True) | Q(ended_at__gte=reference_time))
        .values_list('id', flat=True)
    )

    active_partner_ids, ended_partner_ids = get_partner_ids_by_status(user, reference_time)

    total_partners_count = len(active_partner_ids)
    indirect_partners_count = max(total_partners_count - len(direct_partner_ids), 0)

    return (
        len(direct_partner_ids),
        indirect_partners_count,
        total_partners_count,
        len(ended_partner_ids),
    )


def annotate_partner_profiles(users_profiles, reference_time=None):
    """Annotate direct partner profiles with partner counts and active status."""

    if reference_time is None:
        reference_time = timezone.now()

    total_partners = 0

    for partner_profile in users_profiles:
        partner_count = Profile.objects.filter(
            user__create_by=partner_profile.user
        ).count()
        partner_profile.partner_count = partner_count

        ended_at = partner_profile.user.ended_at
        partner_profile.is_active_partner = (
            ended_at is None or ended_at >= reference_time
        )

        total_partners += partner_count

    return total_partners


    
    
    

#profile
@login_required
def profile(request):
    user = request.user
    
    user_profile = Profile.objects.get(user=user)
    membership = MemberShip.objects.get(id=user_profile.membership.id)
    #get all memberships that ishidden=False
    memberships = MemberShip.objects.filter(ishidden=False)
    #get all memberships
    allmemberships = MemberShip.objects.all()
    custom_user = CustomUser.objects.get(id=user.id)
    users = CustomUser.objects.filter(create_by=user)
    users_profiles = Profile.objects.filter(user__in=users)
    reference_time = timezone.now()
    total_partners = annotate_partner_profiles(users_profiles, reference_time)


    # #number in school = user_profile.id if user_profile.number=0 elsee user_profile.number
    # my_number = user_profile.id if user_profile.number==0 else user_profile.number
    #get all profile
    allprofiles = Profile.objects.all()
    #get my profile number in all profiles
    my_number = allprofiles.filter(id__lte=user_profile.id).count()
    #number in school = my_number if user_profile.number=0 elsee user_profile.number
    my_number = my_number if user_profile.number==0 else user_profile.number

    my_partners = total_partners + users.count()
    
    #check if mymembership.price is the greatest membership.price
    last = False
    if membership.price == allmemberships.last().price:
        last = True
    
    
    owner=False
    #check if user is superuser and the first user
    if user.is_superuser and user.id==1 :
        owner=True
    
    
    
    direct_partners_ex = users
    (
        direct_partners_count,
        indirect_partners_count,
        total_partners_ex,
        ended_partners_count,
    ) = calculate_partner_counts(user, reference_time)

    rank = Rank.objects.filter(min_number__lte=total_partners_ex).order_by('-min_number').first()
    
    
    context = {
        'owner':owner,
        'number':my_number,
        'profile': user_profile,
        'membership': membership,
        'memberships': memberships,
        'custom_user': custom_user,
        'users': users,
        'users_profiles': users_profiles,
        'total_partners': total_partners,
        'my_partners': my_partners,
        'last':last,
        'direct_partners_ex': direct_partners_ex,
        'direct_partners_count': direct_partners_count,
        'indirect_partners_ex': indirect_partners_count,
        'total_partners_ex': total_partners_ex,
        'rank':rank,
        'ended_partners_count': ended_partners_count,
    }
    return render(request, 'profile.html', context)



#add_new_member
# @login_required
# def add_new_member(request):
#     #if request.method==post get name , email , phone , address , password , birthdate , membership , image , create_by from request.user 
#     if request.method=='POST':
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         phone=request.POST.get('phone')
#         address=request.POST.get('address')
#         password=request.POST.get('password')
#         birthdate=request.POST.get('birthdate')
#         membership=request.POST.get('membership')
#         image=request.FILES.get('image')        
#         create_by=request.user
#          #check if email and phone unique
#         if CustomUser.objects.filter(email=email).exists():
#             #return message "email is exist"
#             messages.error(request, 'email is exist')
#             return redirect('accounts:profile')
#         if CustomUser.objects.filter(phone=phone).exists():
#             #return message "phone is exist"
#             messages.error(request, 'phone is exist')
#             return redirect('accounts:profile')
        
#         #get membership.price        
#         #check if profile.coin => membership.price
#         profile = Profile.objects.get(user=create_by)
#         membershipobject = MemberShip.objects.get(id=membership)
#         if profile.coin < membershipobject.price:
#             #message
#             messages.error(request, 'you dont have enough coin for this membership')
#             return redirect('accounts:profile')
#         else:
#             #profile.coin = profile.coin - membership.price
#             profile.coin = profile.coin - membershipobject.price
#             #profile.save()
#             profile.save()
            
#         #make ended at for me = renewal_days + now
#         create_by.ended_at = timezone.now() + timedelta(days=membershipobject.renewal_days)
#         create_by.save()
        
#         # create user with fields phone , email , create_by
#         user = CustomUser.objects.create_user(phone=phone,email=email,create_by=create_by)
#         #set password for user
#         user.set_password(password)
#         #save user
#         user.save()
#         #get membership instance
#         membershipobject = MemberShip.objects.get(id=membership)
#         #create profile with fields name , address , birthdate , membership , image , user
#         profileobject = Profile.objects.create(name=name,address=address,birth_date=birthdate,membership=membershipobject,price=membershipobject.price,image=image,user=user)
#         #save profile
#         profileobject.save()
        
#         #get myprofile
#         myprofile = Profile.objects.get(user=create_by)
#         # myprofile rank +1
#         myprofile.rank = myprofile.rank + 1
#         #myprofile.save()
#         myprofile.save()
#         #if rank >= 50 then customuser.has_right_sign=true
#         if myprofile.rank >= 50:
#             create_by.has_right_sign = True
#             create_by.save()
#     #redirct to profile
#     return redirect('accounts:profile')

import unicodedata


@login_required
def add_new_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        membership = request.POST.get('membership')
        image = request.FILES.get('image')
        create_by = request.user
        # Check if email and phone are unique
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('accounts:profile')
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone already exists')
            return redirect('accounts:profile')

        profile = Profile.objects.get(user=create_by)
        membershipobject = MemberShip.objects.get(id=membership)

        if profile.coin < membershipobject.price:
            messages.error(request, 'You don\'t have enough coins for this membership')
            return redirect('accounts:profile')

        # Normalize the name to ASCII characters
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        #         # Normalize the name to ASCII characters


        user = CustomUser.objects.create_user(phone=phone, email=email, create_by=create_by)
        user.set_password(password)
        user.save()

        membershipobject = MemberShip.objects.get(id=membership)
        
        
        
        # Generate a unique filename using a UUID and the original file extension
        _, file_extension = os.path.splitext(image.name)
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"

        
        try:
            profileobject = Profile.objects.create(name=name, address=address, birth_date=birthdate,
                                              membership=membershipobject, price=membershipobject.price,
                                               user=user)
            profileobject.image.save(unique_filename, image)
            profileobject.save()
        except:
            #delete user
            if user:
                user.delete()
            messages.error(request, 'Error creating profile')
            return redirect('accounts:profile')

        profile.coin = profile.coin - membershipobject.price
        profile.save()

        extend_membership_for_direct_partner(create_by)

        myprofile = Profile.objects.get(user=create_by)
        myprofile.rank = myprofile.rank + 1
        myprofile.save()

        if myprofile.rank >= 50:
            create_by.has_right_sign = True
            create_by.save()
            
        
        #get welcome message
        wellcome_message2 = wellcome_message.objects.first()    
        
        #send welcome email to user with email , password
        message = ' '
        subject = 'Welcome to Trading Whale School'
        if wellcome_message2:
            message = wellcome_message2.message
            message+='\n'
            
            message+=f'Email: {email}\n'
            message+=f'Password: {password}\n\n'
            message+=f'{settings.BASE_URL}\n\n'
        
        else:
            message = (
                f'Hello {email},\n\n'
                'Welcome to Trading Whale School!\n'
                'Your account has been created successfully.\n\n'
                'Your login details are as follows:\n'
                f'Email: {email}\n'
                f'Password: {password}\n\n'
                #link
                f'{settings.BASE_URL}\n\n'
                'Thank you for using Trading Whale School!\n'
                'Best regards,\n'
                'The Trading Whale School Team'
            )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('accounts:profile')



#forget_pass
def forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            #get profile 
            profile = Profile.objects.get(user=user)
            username= False
            #check if profile
            if profile:
                username=profile.name
            else:
                username=user.email
                
            #check if user is blocked
            if user.is_blocked:
                messages.error(request, 'Your account is currently blocked, and password reset is not available.')
                return redirect('accounts:forget_pass')
            
            # Send the password reset email
            subject = 'Password Reset Request for Trading Whale School Account'
            
            message = ' '
            
            reset_message = reset_password_message.objects.first()
            if reset_message:
                message = reset_message.message
                message+='\n'
                
                message+=f'{settings.BASE_URL}/accounts/en/reset-password/{user.id}/\n'
                
            else:
                message = (
                    f'Hello {username},\n\n'
                    'You are receiving this email because a password reset request was made for your account on Trading Whale School.\n'
                    'If you did not initiate this request, you can safely ignore this email.\n\n'
                    'To reset your password, please click on the link below:\n'
                    f'{settings.BASE_URL}/accounts/en/reset-password/{user.id}/\n\n'
                    'Thank you for using Trading Whale School!\n'
                    'Best regards,\n'
                    'The Trading Whale School Team'
                )
            
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            messages.success(request, 'We have sent you a password reset email. Please check your inbox.')
            return redirect('accounts:forget_pass')
        else:
            messages.error(request, 'An account with this email address does not exist.')
            return redirect('accounts:forget_pass')
    return render(request, 'forget-pass.html')


#reset-password
def reset_password(request,id):
    #get user by id
    user = CustomUser.objects.get(id=id)
    #if request.method==post
    if request.method=='POST':
        #get password from request
        password = request.POST.get('password')
        #set password for user
        user.set_password(password)
        #save user
        user.save()
        #message
        messages.success(request, 'your password has been reset')
        #redirct to login
        return redirect('accounts:login')
    return render(request,'reset-password.html')


#send coin
@login_required
def send_coin(request):
    #send coin from request.user to user that send phone in the requesr
    if request.method=='POST':
        #get phone , coin from request
        phone = request.POST.get('phone')
        coin = request.POST.get('coin')
        #check if phone exist
        if CustomUser.objects.filter(phone=phone).exists():
            #get user from phone
            user = CustomUser.objects.get(phone=phone)
            #get profile from user
            profile = Profile.objects.get(user=user)
            #get coin that request.user have
            #check if coin that request.user have => coin
            if request.user.profile.coin < int(coin):
                messages.error(request, 'you dont have enough coin')
                return redirect('accounts:profile')
        
            #check if user is not superuser
            if not request.user.is_superuser: 
                #check if market_avilable is false
                if not profile.marketing_avilable:
                    messages.error(request, 'this user is not avilable for marketing')
                    return redirect('accounts:profile')
            
            #check if coin mod any membership.price !=0
            memberships = MemberShip.objects.all()
            for membership in memberships:
                if int(coin) % membership.price == 0:
                    break
            else:
                messages.error(request, 'you can send coin only membership price or multiple of membership price')
                return redirect('accounts:profile')
            
            #request.user.profile.coin-coin
            request.user.profile.coin = request.user.profile.coin - int(coin)
            request.user.profile.save()
             
            #profile.coin = profile.coin + coin
            profile.coin = profile.coin + int(coin)
            #profile.save()
            profile.save()
        
            #check if user isblocked
            if user.is_blocked:
                profile.coin = profile.coin - 50
                profile.save()
                #unblock
                user.is_blocked = False
                #ended_at +30 day
                user.ended_at = user.ended_at + timedelta(days=30)
                user.save()
            
            #message
            return redirect('accounts:profile')
        else:
            return redirect('accounts:profile')
        
    return redirect('accounts:profile')



@login_required
def team_profile(request,id):
    viewed_user = get_object_or_404(CustomUser, id=id)

    if not request.user.is_superuser and request.user != viewed_user:
        active_partner_ids, ended_partner_ids = get_partner_ids_by_status(request.user)
        allowed_partner_ids = active_partner_ids | ended_partner_ids

        if viewed_user.id not in allowed_partner_ids:
            messages.error(request, 'You do not have permission to view this team.')
            return redirect('accounts:profile')

    user_profile = get_object_or_404(Profile, user=viewed_user)
    membership = user_profile.membership
    memberships = MemberShip.objects.all()
    custom_user = viewed_user
    users = CustomUser.objects.filter(create_by=viewed_user)
    users_profiles = Profile.objects.filter(user__in=users)
    reference_time = timezone.now()


    forign=1
    total_partners = annotate_partner_profiles(users_profiles, reference_time)

    my_partners = total_partners + users.count()

    direct_partners_ex = users
    (
        direct_partners_count,
        indirect_partners_count,
        total_partners_ex,
        ended_partners_count,
    ) = calculate_partner_counts(viewed_user, reference_time)
    
        
    
    
    context = {
        'profile': user_profile,
        'membership': membership,
        'memberships': memberships,
        'custom_user': custom_user,
        'users': users,
        'users_profiles': users_profiles,
        'total_partners': total_partners,
        'my_partners': my_partners,
        'forign':forign,
        'direct_partners_ex': direct_partners_ex,
        'direct_partners_count': direct_partners_count,
        'indirect_partners_ex': indirect_partners_count,
        'total_partners_ex': total_partners_ex,
        'ended_partners_count': ended_partners_count,
    }
    return render(request, 'profile.html', context)


@login_required
#upgrade_membership
def upgrade_membership(request):
    profile = Profile.objects.get(user=request.user)
    #get membership for this user
    mymembership = MemberShip.objects.get(id=profile.membership.id)
    #get the next membership in memberships that have price > mymembership.price
    memberships = MemberShip.objects.filter(price__gt=mymembership.price)
    #if memberships is not empty
    if memberships:
        #get the first membership
        membership = memberships.first()
        #if profile.coin < membership.price
        if profile.coin < membership.price - profile.coin :
            #message
            messages.error(request, 'you dont have enough coin for this membership')
            return redirect('accounts:profile')
        else:
            removed_coin = membership.price - mymembership.price
            
        
            #profile.coin = profile.coin - removed_coin
            profile.coin = profile.coin - removed_coin
            #profile.save()
            profile.save()
            #profile.membership = membership
            profile.membership = membership
            #profile.price = membership.price
            profile.price = membership.price
            #profile.save()
            profile.save()
            #message
            messages.success(request, 'you have upgrade your membership')
            return redirect('accounts:profile')
    else:
        #message
        messages.error(request, 'you on the last membership')
        return redirect('accounts:profile')
    #redirct to profile
    return redirect('accounts:profile')



import uuid

def changeimage(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        profile = Profile.objects.get(user=request.user)
        
        # Generate a unique filename using a UUID and the original file extension
        _, file_extension = os.path.splitext(image.name)
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        
        # Save the file with the unique filename
        profile.image.save(unique_filename, image)
        
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')
#================================AR===============================================

#log_in 
def log_in_ar(request):
    #login 
    if request.method == 'POST':
        #get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticate user
        user = authenticate(request, username=username, password=password)
        access=False
        
        if user is not None:
            access=True
        else:
            #send message
            messages.error(request, 'بيانات تسجيل الدخول غير صحيحه')
            return render(request,'ar/index.html')
    #check if user is blocked
        if user.is_blocked:
            #send message
            messages.error(request, "عزيز المتداول نود اعلامك بان فترة التعليم الخاصة بك في موقع حيتان التداول قد انتهت اذا كنت ترغب في تجديد الاشتراك والاستمرار في رحلتك التعليمية معنا يرجي التواصل مع الشخص المسئول الكوتش بتاعك ليطلعك علي خطوات التجديد شكرا لاختيارك حيتان التداول ونتطلع لمواصلة دعمك وتقديم افضل تجربة تعليمية لك تحياتنا فريق حيتان التداول")
            return render(request,'ar/index.html')

        if user.ended_at and user.ended_at < timezone.now():
            messages.error(request, 'تم انتهاء الخطه الخاصه بك عد للمسؤلين لتجديد الخطه')
            return render(request,'ar/index.html')


        #if access = True login
        if access:
            login(request, user)
            #redirct to profile
            return redirect('home:home_ar')

    return render(request,'ar/index.html')

#log_out
#login_required
@login_required
def log_out_ar(request):
    logout(request)
    #redirct to login 
    return redirect('accounts:login_ar')
    
#profile
@login_required
def profile_ar(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    membership = MemberShip.objects.get(id=user_profile.membership.id)
    #get all memberships that ishidden=False
    memberships = MemberShip.objects.filter(ishidden=False)
    #get all memberships
    allmemberships = MemberShip.objects.all()
    
    custom_user = CustomUser.objects.get(id=user.id)
    users = CustomUser.objects.filter(create_by=user)
    users_profiles = Profile.objects.filter(user__in=users)
    reference_time = timezone.now()
    total_partners = annotate_partner_profiles(users_profiles, reference_time)

    my_partners = total_partners + users.count()
    
    
    my_number = user_profile.id if user_profile.number==0 else user_profile.number


    #get all profile
    allprofiles = Profile.objects.all()
    #get my profile number in all profiles
    my_number = allprofiles.filter(id__lte=user_profile.id).count()
    #number in school = my_number if user_profile.number=0 elsee user_profile.number
    my_number = my_number if user_profile.number==0 else user_profile.number
    
    #check if mymembership.price is the greatest membership.price
    last = False
    if membership.price == allmemberships.last().price:
        last = True
        
        
    owner=False
    #check if user is superuser and the first user
    if user.is_superuser and user.id==1 :
        owner=True    
    
    
    direct_partners_ex = users
    (
        direct_partners_count,
        indirect_partners_count,
        total_partners_ex,
        ended_partners_count,
    ) = calculate_partner_counts(user, reference_time)


    rank = Rank.objects.filter(min_number__lte=total_partners_ex).order_by('-min_number').first()

    
    
    context = {
        'owner':owner,
        'number':my_number,
        'profile': user_profile,
        'membership': membership,
        'memberships': memberships,
        'custom_user': custom_user,
        'users': users,
        'users_profiles': users_profiles,
        'total_partners': total_partners,
        'my_partners': my_partners,
        'last':last,
        'indirect_partners_ex': indirect_partners_count,
        'direct_partners_count': direct_partners_count,
        'direct_partners_ex': direct_partners_ex,
        'total_partners_ex': total_partners_ex,
        'rank':rank,
        'ended_partners_count': ended_partners_count,
    }
    return render(request, 'ar/profile.html', context)

#add_new_member
@login_required
def add_new_member_ar(request):
    #if request.method==post get name , email , phone , address , password , birthdate , membership , image , create_by from request.user 
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        password=request.POST.get('password')
        birthdate=request.POST.get('birthdate')
        membership=request.POST.get('membership')
        image=request.FILES.get('image')        
        create_by=request.user
         #check if email and phone unique
        if CustomUser.objects.filter(email=email).exists():
            #return message "email is exist"
            messages.error(request, 'الايميل مستخدم من قبل')
            return redirect('accounts:profile')
        if CustomUser.objects.filter(phone=phone).exists():
            #return message "phone is exist"
            messages.error(request, 'رقم الهاتف مستخدم من قبل')
            return redirect('accounts:profile_ar')
        
        #get membership.price        
        #check if profile.coin => membership.price
        profile = Profile.objects.get(user=create_by)
        membershipobject = MemberShip.objects.get(id=membership)
        if profile.coin < membershipobject.price:
            #message
            messages.error(request, 'لا تمتلك عدد كافي من النقاط لهذا العضوية')
            return redirect('accounts:profile_ar')


       
        
        # create user with fields phone , email , create_by
        user = CustomUser.objects.create_user(phone=phone,email=email,create_by=create_by)
        #set password for user
        user.set_password(password)
        #save user
        user.save()
        
        # Normalize the name to ASCII characters
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        
        #get membership instance
        membershipobject = MemberShip.objects.get(id=membership)
        
        # Generate a unique filename using a UUID and the original file extension
        _, file_extension = os.path.splitext(image.name)
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        #create profile with fields name , address , birthdate , membership , image , user
        try:
            profileobject = Profile.objects.create(name=name,address=address,birth_date=birthdate,membership=membershipobject,price=membershipobject.price,user=user)
            # Save the image file with the unique filename
            profileobject.image.save(unique_filename, image)
        #save profile
            profileobject.save()
        except:
            #delete user
            if user:
                user.delete()
            messages.error(request, 'حدث خطأ في انشاء الحساب' )
            return redirect('accounts:profile_ar')
        
        profile.coin = profile.coin - membershipobject.price
        #profile.save()
        profile.save()

        extend_membership_for_direct_partner(create_by)
        #get myprofile
        myprofile = Profile.objects.get(user=create_by)
        # myprofile rank +1
        myprofile.rank = myprofile.rank + 1
        #myprofile.save()
        myprofile.save()
        #if rank >= 50 then customuser.has_right_sign=true
        if myprofile.rank >= 50:
            create_by.has_right_sign = True
            create_by.save()
        #send welcome email to user with email , password
        subject = 'مدرسة حيتان التداول'
        wellcome_message2 = wellcome_message.objects.first()  
        message=" "
        if wellcome_message2:
            message = wellcome_message2.message_ar
            message+= f'\n\n'
            message+=f'الايميل: {email}\n'
            message+=f'كلمة المرور: {password}\n'
            message+=f' الرابط: {settings.BASE_URL}\n'
        else:
            message = (
                f'مرحبا {email},\n\n'
                'تم انشاء حسابك بنجاح في مدرسة حيتان التداول.\n'
                'تم انشاء حسابك بنجاح.\n\n'
                'بيانات تسجيل الدخول الخاصة بك هي كالتالي:\n'
                f'الايميل: {email}\n'
                f'كلمة المرور: {password}\n\n'
                #link
                f'{settings.BASE_URL}\n\n'
                'شكرا لاستخدامك مدرسة حيتان التداول!\n'
                'فريق عمل مدرسة حيتان التداول'
            )
        
        #send email
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    #redirct to profile
    return redirect('accounts:profile_ar')



#forget_pass
def forget_pass_ar(request):
    #if request post message we have send link for you
    if request.method=='POST':
        #get phone from request
        email = request.POST.get('email')
        #check if phone exist
        if CustomUser.objects.filter(email=email).exists():
            #get user from phone
            user = CustomUser.objects.get(email=email)
            #check if user is blocked
            if user.is_blocked:
                #message
                messages.error(request, 'حسابك محظور لا يمكنك تغيير كلمة المرور')
                return redirect('accounts:forget_pass_ar')
            #check if user is blocked
            if user.is_blocked:
                #message
                messages.error(request, 'حسابك محظور لا يمكنك تغيير كلمة المرور')
                return redirect('accounts:forget_pass_ar')
            
            # Send the password reset email
            subject = 'طلب تغيير كلمة المرور لحسابك في مدرسة حيتان التداول'
            
            
            message=" "
            reset_message = reset_password_message.objects.first()  
            if reset_message:
                message = reset_message.message_ar
                message+='\n'
                
                message+=f'{settings.BASE_URL}/accounts/ar/reset-password/{user.id}/\n'
            else:
                message = (
                    f'مرحبا {user.email},\n\n'
                    'انت تستلم هذا الايميل لانك طلبت تغيير كلمة المرور لحسابك في مدرسة حيتان التداول.\n'
                    'اذا لم تطلب تغيير كلمة المرور يمكنك تجاهل هذا الايميل.\n\n'
                    'لتغيير كلمة المرور الرجاء الضغط على الرابط التالي:\n'
                    f'{settings.BASE_URL}/accounts/ar/reset-password/{user.id}/\n\n'
                    'شكرا لاستخدامك مدرسة حيتان التداول!\n'
                    'فريق عمل مدرسة حيتان التداول'
                )
            
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            #message
            messages.success(request, 'تم ارسال رابط تغيير كلمة المرور الي بريدك الالكتروني')
            return redirect('accounts:forget_pass_ar')
        else:
            #message
            messages.error(request, 'لا يوجد حساب بهذا الايميل')
            return redirect('accounts:forget_pass_ar')
    return render(request,'ar/forget-pass.html')





#send coin
@login_required
def send_coin_ar(request):
    #send coin from request.user to user that send phone in the requesr
    if request.method=='POST':
        #get phone , coin from request
        phone = request.POST.get('phone')
        coin = request.POST.get('coin')
        #check if phone exist
        if CustomUser.objects.filter(phone=phone).exists():
            #get user from phone
            user = CustomUser.objects.get(phone=phone)
            #get profile from user
            profile = Profile.objects.get(user=user)
            #get coin that request.user have
            #check if coin that request.user have => coin
            if request.user.profile.coin < int(coin):
                messages.error(request, 'ليس لديك عملات كافية')
                return redirect('accounts:profile_ar')
            #check if user is not superuser
            if not request.user.is_superuser: 
                #check if market_avilable is false
                if not profile.marketing_avilable:
                    messages.error(request, 'هذا المستخدم غير متاح للتسويق')
                    return redirect('accounts:profile_ar')
            
             #check if coin mod any membership.price !=0
            memberships = MemberShip.objects.all()
            for membership in memberships:
                if int(coin) % membership.price == 0:
                    break
            else:
                messages.error(request, 'يمكنك ارسال عدد من العملات يساوي سعر العضوية او مضاعفاتها فقط')
                return redirect('accounts:profile_ar')
            
            
            #check is not super user request.user.profile.coin-coin
            
            request.user.profile.coin = request.user.profile.coin - int(coin)
            request.user.profile.save()
             
            #profile.coin = profile.coin + coin
            profile.coin = profile.coin + int(coin)
            #profile.save()
            profile.save()
        
            #check if user isblocked
            if user.is_blocked:
                profile.coin = profile.coin - 50
                profile.save()
                #unblock
                user.is_blocked = False
                #ended_at +30 day
                user.ended_at = user.ended_at + timedelta(days=30)
                user.save()
            
            #message
            return redirect('accounts:profile_ar')
        else:
            return redirect('accounts:profile_ar')
        
    return redirect('accounts:profile_ar')



@login_required
def team_profile_ar(request,id):
    viewed_user = get_object_or_404(CustomUser, id=id)

    if not request.user.is_superuser and request.user != viewed_user:
        active_partner_ids, ended_partner_ids = get_partner_ids_by_status(request.user)
        allowed_partner_ids = active_partner_ids | ended_partner_ids

        if viewed_user.id not in allowed_partner_ids:
            messages.error(request, 'غير مصرح لك بعرض هذه الصفحة.')
            return redirect('accounts:profile_ar')

    user_profile = get_object_or_404(Profile, user=viewed_user)
    membership = user_profile.membership
    memberships = MemberShip.objects.all()
    custom_user = viewed_user
    users = CustomUser.objects.filter(create_by=viewed_user)
    users_profiles = Profile.objects.filter(user__in=users)
    reference_time = timezone.now()
    forign=1
    total_partners = annotate_partner_profiles(users_profiles, reference_time)

    my_partners = total_partners + users.count()

    direct_partners_ex = users
    (
        direct_partners_count,
        indirect_partners_count,
        total_partners_ex,
        ended_partners_count,
    ) = calculate_partner_counts(viewed_user, reference_time)
    
    
    
    
    context = {
        'profile': user_profile,
        'membership': membership,
        'memberships': memberships,
        'custom_user': custom_user,
        'users': users,
        'users_profiles': users_profiles,
        'total_partners': total_partners,
        'my_partners': my_partners,
        'forign':forign,
        'direct_partners_ex': direct_partners_ex,
        'direct_partners_count': direct_partners_count,
        'indirect_partners_ex': indirect_partners_count,
        'total_partners_ex': total_partners_ex,
        'ended_partners_count': ended_partners_count,

    }
    return render(request, 'ar/profile.html', context)


@login_required
#upgrade_membership
def upgrade_membership_ar(request):
    profile = Profile.objects.get(user=request.user)
    #get membership for this user
    mymembership = MemberShip.objects.get(id=profile.membership.id)
    #get the next membership in memberships that have price > mymembership.price
    memberships = MemberShip.objects.filter(price__gt=mymembership.price)
    #if memberships is not empty
    if memberships:
        #get the first membership
        membership = memberships.first()
        #if profile.coin < membership.price
        if profile.coin < membership.price - profile.coin :
            #message
            messages.error(request, 'لا تمتلك عملات كفاية لهذه العضوية')
            return redirect('accounts:profile_ar')
        else:
            removed_coin = membership.price - mymembership.price
            
        
            #profile.coin = profile.coin - removed_coin
            profile.coin = profile.coin - removed_coin
            #profile.save()
            profile.save()
            #profile.membership = membership
            profile.membership = membership
            profile.price = membership.price
            #profile.save()
            profile.save()
            #message
            messages.success(request, 'تم ترقية عضويتك بنجاح')
            return redirect('accounts:profile_ar')
    else:
        #message
        messages.error(request, 'انت في اعلى عضوية')
        return redirect('accounts:profile_ar')
    #redirct to profile
    return redirect('accounts:profile_ar')


def reset_password_ar(request,id):
    #get user by id
    user = CustomUser.objects.get(id=id)
    #if request.method==post
    if request.method=='POST':
        #get password from request
        password = request.POST.get('password')
        #set password for user
        user.set_password(password)
        #save user
        user.save()
        #message
        messages.success(request, 'تم تغيير كلمة المرور بنجاح')
        #redirct to login
        return redirect('accounts:login_ar')
    return render(request,'ar/reset-password.html')
