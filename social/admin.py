from django.contrib import admin
from social.models import Post,Comment,UserProfile
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
