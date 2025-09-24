from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from users.models import CustomUser

from .models import Contact


def _resolve_profiles(user):
    """Return profile information for the current user and their creator."""

    custom_user = (
        CustomUser.objects.select_related("create_by")
        .only("email", "ended_at", "create_by")
        .get(id=user.id)
    )

    my_profile = Profile.objects.select_related("user").filter(user=user).first()

    created_by_profile = None
    created_by_name = ""

    if not user.is_superuser and custom_user.create_by:
        created_by_profile = Profile.objects.filter(user=custom_user.create_by).first()
        if created_by_profile:
            created_by_name = created_by_profile.name
        else:
            created_by_name = custom_user.create_by.email
    elif my_profile:
        created_by_profile = my_profile
        created_by_name = my_profile.name

    if not created_by_name:
        created_by_name = my_profile.name if my_profile else custom_user.email

    return my_profile, custom_user, created_by_profile, created_by_name, custom_user.ended_at


def _handle_contact(request, *, template_name, success_message, contact_redirect,
                    profile_redirect, missing_profile_message):
    """Shared logic for English and Arabic contact pages."""

    my_profile, custom_user, created_by_profile, created_by_name, ended_at = _resolve_profiles(request.user)

    if my_profile is None:
        messages.error(request, missing_profile_message)
        return redirect(profile_redirect)

    if request.method == "POST":
        subject = (request.POST.get("subject") or "").strip()
        message_body = (request.POST.get("message") or "").strip()

        Contact.objects.create(
            name=my_profile.name,
            email=custom_user.email,
            create_by=created_by_name,
            ended_at=ended_at,
            subject=subject,
            message=message_body,
        )

        messages.success(request, success_message)
        return redirect(contact_redirect)

    context = {
        "profile": my_profile,
        "my_profile": my_profile,
        "custom_user": custom_user,
        "created_by": created_by_profile,
        "created_by_name": created_by_name,
        "ended_at": ended_at,
    }

    return render(request, template_name, context)


# Create your views here.


@login_required
def contact(request):
    return _handle_contact(
        request,
        template_name="contact.html",
        success_message="your message has been sent successfully",
        contact_redirect="contact:contact",
        profile_redirect="accounts:profile",
        missing_profile_message="Please complete your profile before contacting support.",
    )


# =======================================AR========================================


@login_required
def contact_ar(request):
    return _handle_contact(
        request,
        template_name="ar/contact.html",
        success_message="تم ارسال رسالتك بنجاح",
        contact_redirect="contact:contact_ar",
        profile_redirect="accounts:profile_ar",
        missing_profile_message="يرجى استكمال ملفك الشخصي قبل التواصل معنا.",
    )
