from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,AbstractUser,PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    #add create_user method
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('The Email or Phone field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        #set password with make_password method
        user.set_password(password)
        user.create_at=timezone.now()
        #check if superuser end_date=none
        if user.is_superuser:
            user.ended_at=None
        else:
            user.ended_at=timezone.now()+timezone.timedelta(days=90)
        user.save(using=self._db)
        
        return user
    #add create_superuser method
    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #set is_active = true
        extra_fields.setdefault('is_active', True)
        #set is_blocked = false
        extra_fields.setdefault('is_blocked', False)
        #set has_right_sign = true
        extra_fields.setdefault('has_right_sign', True)
        #set end_at with null
        extra_fields.setdefault('ended_at', None)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password, **extra_fields)
    #add update_user method
    def update_user(self, email, phone, password=None, **extra_fields):
        pass
    
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    create_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True,blank=True)
    is_blocked = models.BooleanField(default=False)
    has_right_sign = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    has_landpage= models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def is_user_blocked(self):
        return self.is_blocked

    def has_user_right_sign(self):
        return self.has_right_sign
    
    #return name
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['id']
    
    
    

