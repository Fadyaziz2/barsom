from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone


class MembershipExpirationMiddleware:
    """Ensure authenticated users with expired memberships are logged out."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user is not None and user.is_authenticated:
            ended_at = getattr(user, "ended_at", None)

            if ended_at and ended_at < timezone.now():
                logout(request)
                messages.error(
                    request,
                    "Your plan has ended. Please contact the administrators to renew your plan.",
                )
                return redirect("accounts:login")

        return self.get_response(request)
