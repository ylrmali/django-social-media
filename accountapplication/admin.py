from django.contrib import admin
from .models import Post, User, Comment, Profile, Notification

# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Notification)

