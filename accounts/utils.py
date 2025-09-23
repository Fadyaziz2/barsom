"""Utility helpers for working with user profiles."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Optional, Tuple

from django.shortcuts import render

from .models import Profile


def _build_admin_placeholder_profile(user):
    """Create a lightweight profile-like object for staff users without profiles."""

    membership_placeholder = SimpleNamespace(name="Not assigned", price=0)

    placeholder = SimpleNamespace(
        user=user,
        membership=membership_placeholder,
        name=getattr(user, "get_full_name", lambda: "")()
        or getattr(user, "username", "")
        or getattr(user, "email", ""),
        address="",
        birth_date="",
        coin=0,
        image=None,
        price=0,
        marketing_avilable=False,
        rank=0,
        number=0,
        is_placeholder=True,
    )

    return placeholder


def get_profile_or_missing_response(request, language: str = "en") -> Tuple[Optional[Profile], Optional[object]]:
    """Return the logged-in user's profile or a fallback response if it is missing.

    The helper mirrors the logic previously used in multiple view functions:

    * Authenticated users with a completed profile get their profile instance.
    * Staff and superusers without a profile receive a lightweight placeholder so
      they can continue navigating the dashboard.
    * Regular users without a profile are shown a friendly "profile missing"
      page in their preferred language instead of a server error.
    """

    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", False):
        return None, None

    profile = (
        Profile.objects.select_related("membership")
        .filter(user=user)
        .first()
    )
    if profile is not None:
        profile.is_placeholder = False
        return profile, None

    if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
        return _build_admin_placeholder_profile(user), None

    template_name = "profile_missing.html" if language != "ar" else "ar/profile_missing.html"
    return None, render(request, template_name, status=404)

