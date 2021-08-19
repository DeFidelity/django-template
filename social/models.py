from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',related_name='profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.CharField(max_length=100,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures',default='uploads/profile_pictures/default.png',blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')



@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance,**kwargs):
    instance.profile.save()
