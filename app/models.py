from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your views here.


class User(AbstractUser):

    role_choices = (
        ('student', 'Student'),
        ('staff', 'Staff'),
    )
    user = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile_images')
    role = models.CharField(max_length=100 ,choices=role_choices)
    friends = models.ManyToManyField('Friend', related_name='my_friends', null=True, blank=True )
    
    REQUIRED_FIELDS = []



@receiver(post_save, sender=User)
def add_friend_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # Create a Friend instance for the user and add it to the user's friends
        Friend.objects.create(profile=instance)


class Friend(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.profile.user
    

    
class Event(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    

class News(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)



class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_sender')    
    msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_receiver')    
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class CommunityForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.CharField(max_length=100)
    image = models.ImageField(upload_to='community', null=True, blank=True)

    
    def __str__(self):
        return self.msg
    
class Books(models.Model):
    File_Type = (
        ('pdf', 'PDF'),
        ('ppt', 'PPT'),
        ('xls', 'XLS'),
        ('doc', 'DOC'),
        ('video', 'VIDEO'),
        ('image', 'IMAGE'),
        ('text', 'Text'),
    )
    title = models.CharField(max_length= 100, default='book_titel')
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file_send' , null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    

    

class Complain(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 100)
    description = models.TextField(null=True, blank=True)
    
