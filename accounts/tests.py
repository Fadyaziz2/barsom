from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class SuperuserExpiredMembershipAccessTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.password = "StrongPass123!"
        self.superuser = self.User.objects.create_superuser(
            email="admin@example.com",
            phone="1000000000",
            password=self.password,
        )
        self.superuser.ended_at = timezone.now() - timedelta(days=1)
        self.superuser.save(update_fields=["ended_at"])

    def test_expired_superuser_can_log_in(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.superuser.email, "password": self.password},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home:home_ar"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.superuser.id)

    def test_expired_superuser_is_not_logged_out_by_membership_middleware(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("accounts:profile"))

        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.superuser.id)
