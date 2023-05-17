from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.BigIntegerField(unique=True, blank=True, null=True)
    password = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(blank=True, null=True, upload_to='profile-photos')
    background_photo = models.ImageField(blank=True, null=True, upload_to='background-photos')
    last_online = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_lock = models.BooleanField(default=False)
    follower = models.ManyToManyField(User,  blank=True, null=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, null=True, related_name='followings')

    def get_followers(self):
        return self.follower.all()
    
    def get_following(self):
        return self.following.all()
    
    def __str__(self):
        return f'{self.user.username} Profile'



class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    post_text = models.TextField(max_length=500, blank=True, null=True)
    post_media = models.FileField(blank=True, null=True, upload_to='post-images')
    is_active = models.BooleanField(default=True)
    like_owner = models.ManyToManyField(User, related_name='post_like', null=True, blank=True)
    comment_owner = models.ManyToManyField(User, related_name='post_comment', null=True, blank=True)

    def __str__(self):
        return f"{self.created_time}"


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=250, blank=True, null=True)
    like_owner = models.ManyToManyField(User, related_name='likeOwner')
    created_time = models.DateTimeField(auto_now_add=True)

