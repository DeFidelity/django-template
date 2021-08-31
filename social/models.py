from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    shared_body = models.TextField(blank=True,null=True)
    body = models.TextField()
    image = models.ManyToManyField('Image',blank=True,)
    created_on = models.DateTimeField(default=timezone.now)
    shared_on =models.DateTimeField(blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='+')
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name='dislikes')
    tags = models.ManyToManyField('Tag',blank=True)

    def create_tag(self):
        for word in self.body.split():
            if word[0] == '#':
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
            self.save()

    class Meta:
        ordering = ['-created_on','-shared_on']

    def __str__(self):
        return self.body

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True,related_name='comment_likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name='comment_dislikes')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')
    tags = models.ManyToManyField('Tag',blank=True)


    def create_tag(self):
        for word in self.comment.split():
            if word[0] == '#':
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
            self.save()


    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user',related_name='profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.CharField(max_length=100,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/profile_pictures',default='uploads/profile_pictures/default.png',blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


    def __str__(self):
        return self.name


@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance,**kwargs):
    instance.profile.save()


class Notification(models.Model):
    # 1=like, 2=comment, 3=follow, 4=message
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User,related_name='notification_to',on_delete=models.CASCADE,null=True)
    from_user = models.ForeignKey(User,related_name='notification_from',on_delete=models.CASCADE,null=True)
    post = models.ForeignKey('Post',related_name='+',on_delete=models.CASCADE,null=True,blank=True)
    thread = models.ForeignKey('ThreadModel',related_name='+',on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey('Comment',related_name='+',on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification_type)

class ThreadModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')


class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel',related_name='+',on_delete=models.CASCADE,blank=True,null=True)
    sender_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    receiver_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    body = models.CharField(max_length=1000,)
    image  = models.ImageField(upload_to='uploads/message_photos',blank=True,null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.thread

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photo',blank=True,null=True)

class Tag(models.Model):
    name = models.CharField(max_length=60)
