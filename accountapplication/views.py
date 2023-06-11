from django.shortcuts import render, redirect, HttpResponse
from accountapplication.models import User, Post, Profile


# Create your views here.


# home page
def index(request):
    target_user = Profile.objects.get(user=1)  # target user / who's profile will load
    id = Profile.objects.get(user='asd').id  # target user id
    posts = Post.objects.filter(owner=id)  # target user's posts
    post_count = posts.count()  # target user's post count
    # is the current user following the target user?
    tu_is_follower = target_user.follower.filter(username=request.user).exists()  # is current user a follower?
    followers = list(target_user.follower.values('id', 'username', 'first_name', 'last_name', 'profile_photo'))
    context = {
        'follower': followers,
    }
    return render(request, 'accountapplication/index.html')


# user profile page
def profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        target_user = Profile.objects.get(user=user_id)   # target user / who's profile will load
        id = Profile.objects.get(user=user_id).id       # target user id
        posts = Post.objects.filter(owner_id=user_id)               # target user's posts
        post_count = posts.count()                          # target user's post count
        follower_count = target_user.follower.count()       # target user's follower count
        following_count = target_user.following.count()     # target user's following count
        # is the current user following the target user?
        tu_is_follower = target_user.follower.filter(username=request.user.username).exists()  # is current user a follower?
        context = {
            'user_data': user,
            'profile_data': target_user,
            'user_post': posts,
            'post_count': post_count,
            'follower_count': follower_count,
            'following_count': following_count,
            'user_id': id,
            'is_follower': tu_is_follower,    
        }

        return render(request, 'accountapplication/profile.html', context)

    except (Profile.DoesNotExist) as err:
        return HttpResponse('Error' + err); 
    


def get_follower(request, username):
    target_user = Profile.objects.get(user=username)  # target user / who's profile will load
    id = Profile.objects.get(user=username).id        # target user id
    posts = Post.objects.filter(owner=id)              # target user's posts
    post_count = posts.count()                         # target user's post count
    follower_count = target_user.follower.count()      # target user's follower count
    following_count = target_user.following.count()    # target user's following count
    # is the current user following the target user?
    tu_is_follower = target_user.follower.filter(username=request.user).exists()  # is current user a follower?
    followers = list(target_user.follower.values('id', 'username', 'first_name', 'last_name'))
    context = {
        'user_data': target_user,
        'user_post': posts,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'user_id': id,
        'is_follower': tu_is_follower,
        'followers': followers,
    }
    return render(request, 'accountapplication/partials/_user_followers.html', context)


def get_following(request, username):
    print(username);
    target_user = Profile.objects.get(user=username)  # target user / who's profile will load
    id = Profile.objects.get(user=username).id        # target user id
    posts = Post.objects.filter(owner=id)              # target user's posts
    post_count = posts.count()                         # target user's post count
    follower_count = target_user.follower.count()      # target user's follower count
    following_count = target_user.following.count()    # target user's following count
    # is the current user following the target user?
    tu_is_follower = target_user.follower.filter(username=request.user).exists()  # is current user a follower?
    follower = target_user.get_following()
    print(follower);
    followings = list(target_user.following.values('id', 'username', 'first_name', 'last_name'))
    context = {
        'user_data': target_user,
        'user_post': posts,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'user_id': id,
        'is_follower': tu_is_follower,
        'followings': followings,
    }
    return render(request, 'accountapplication/partials/_user_following.html', context)

