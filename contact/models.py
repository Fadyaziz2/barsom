from django.db import models


# Create your models here.

#contact model name email added_by ended_at  subject , message

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    create_by = models.CharField(max_length=100)
    ended_at = models.DateTimeField(null=True,blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    def __str__(self):
        return self.name