from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #login with email or phone and password
        try:
            user = User.objects.get(Q(email=username)|Q(phone=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
# Compare this snippet from users\forms.py:

