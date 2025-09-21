from django.db import models
#import validation error
from django.core.exceptions import ValidationError
#import custom_user from users.models
from users.models import CustomUser


# Create your models here.
#membership model with field name , price
class MemberShip(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    #Number of days for renewal default 30 days
    renewal_days=models.IntegerField(default=30)
    #isaactive
    isactive=models.BooleanField(default=False)
    #membership duration
    duration=models.IntegerField(default=90)
    #ishidden
    ishidden=models.BooleanField(default=False)
        #validate price must be mod(50)
    def clean(self):
        if self.price % 50 != 0:
            raise ValidationError('price must be (50,100,150,....)')
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']
    
    
    
class Rank(models.Model):
    name=models.CharField(max_length=100)
    name_ar=models.CharField(max_length=100)
    min_number=models.IntegerField()
    
    def __str__(self):
        return self.name
    
    

#profile model every profile related to user and must has membership plane 
class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    membership=models.ForeignKey(MemberShip,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    birth_date=models.CharField(null=True,blank=True ,max_length=100)
    coin=models.IntegerField(default=0)
    image=models.ImageField(upload_to='static/users/',null=True,blank=True)
    #price
    price=models.FloatField(default=0)
    #new field marketing_avilable
    marketing_avilable=models.BooleanField(default=False)
    #new field rank
    rank=models.IntegerField(default=0)
    #number
    number=models.IntegerField(default=0)
    #no time
    no_time=models.BooleanField(default=False)
    
    #meta ordering by first added
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name    
    
        # # Check if there are any records in the Membership table
        # if MemberShip.objects.count() == 0:
        #     # Create a default Membership record
        #     default_membership = MemberShip.objects.create(name='basic', price=50)
        #     extra_fields['membership'] = default_membership
