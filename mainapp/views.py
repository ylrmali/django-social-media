from django.shortcuts import render, redirect, get_object_or_404
from accountapplication.models import User, Post, Comment
from . forms import CreatePost, CreateComment
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError  # checking error
from itertools import chain  # we convert queryset with list

# Create your views here.

name = 'mainappView'


# home page rendering
# define a try except block because if user didn't log in, we get an error about user not exist
# if user exist, get user's followers id as list. And send to home html with context.
def home(request):
    try:
        current_user = User.objects.get(id=request.user.id)
        user_following_list = []
        post = []

        # get the current user following list ( if ylrmali follow -> yigitali -> it will be in list)
        # define a for loop for append all users id in list.
        user_following = User.objects.filter(follower=current_user.id)
        for users in user_following:
            user_following_list.append(users.id)

        # get users id in user following list.
        # get these user's post.
        # append these posts in post array
        for user_id in user_following_list:
            post_list = Post.objects.filter(owner_id=user_id)
            post.append(post_list)

        posts = list(chain(*post))  # convert queryset to list

        is_liked_list = []
        for post in posts:
            is_liked = (list(post.like_owner.all()).__contains__(request.user))
            is_liked_list.append(is_liked)

        context = {
            'current_user': current_user,
            'posts': posts,
            'is_liked': is_liked_list,
        }
        return render(request, 'mainapp/home.html', context)
    except User.DoesNotExist:
        return render(request, 'mainapp/home.html')


# when user want to create new post, this function will be work
# first check request.method, if method is post -> define a try except block
def check(request):
    if request.method == 'POST':
        owner_id = request.user.id
        # if ['media'] is able to get, it is not empty.
        # so we can save image as post in database.
        try:
            post_image = request.FILES['media']
            post_text = request.POST['post']
            post = Post.objects.create(owner_id=owner_id, post_media=post_image, post_text=post_text)
            post.save()
            return HttpResponse("<p class='alert success'>"
                                "Gönderi başarılı bir şekilde paylaşıldı"
                                "<a class='msg-btn' href='/' >"
                                "<i class='fa-solid fa-xmark' style='color: #ffffff;'></i>"
                                "</a>"
                                "</p>")
        # if server give me multiValueDictKeyError ['media'] its means, your image field if empty.
        # when image is empty save post text in database.
        except MultiValueDictKeyError:
            post_text = request.POST['post']
            post = Post.objects.create(owner_id=owner_id, post_text=post_text)
            post.save()
            return HttpResponse("<p class='alert success'>"
                                "Gönderi başarılı bir şekilde paylaşıldı"
                                "<a class='msg-btn' href='/' >"
                                "<i class='fa-solid fa-xmark' style='color: #ffffff;'></i>"
                                "</a>"
                                "</p>")

    return HttpResponse("<p class='alert error'>"
                        "Boş bir gönderi oluşturulamaz! "
                        "<a class='msg-btn' href='/' >"
                        "<i class='fa-solid fa-xmark' style='color: #ffffff;'></i>"
                        "</a>"
                        "</p>")


# explore page rendering
def explore(request):
    posts = Post.objects.filter(is_active=True)
    context = {
        'posts': posts
    }
    return render(request, 'mainapp/explore.html', context)


# post detail page. I get slug params in url. Check the url.py post-detail function
def post_detail(request, pk):
    if request.method == 'POST':
        form = request.POST['comment_text']
        owner = request.user
        post_id = Post.objects.get(id=pk).id
        comment = Comment.objects.create(comment_text=form, owner=owner, post_id=post_id)
        comment.save()
        return redirect(f'/post/{pk}')
    else:
        form = CreateComment()
        post = Post.objects.get(id=pk)
        comments = Comment.objects.order_by('created_time').filter(post_id=pk)
        comments_count = Comment.objects.filter(post_id=pk).count()
        context = {
            'post': post,
            'comments': comments,
            'comments_count': comments_count,
            'form': form,
        }
        return render(request, 'mainapp/post-detail.html', context)


# post create function
def post_create(request):
    form = CreatePost()
    comment_id = request.GET.get('data-comment-id')
    context = {
        'form': form,
    }
    return render(request, 'mainapp/post-create.html', context)


def post_comment(request, post_id):
    try:
        comment = Comment.objects.filter(post_id=post_id)
        comment_count = comment.count()
        print(comment_count)
        return HttpResponse(comment_count)
    except Comment.DoesNotExist:
        pass
        return HttpResponse('asd')


# comment like function
def like(request,  post_id):
    # checking and getting old liker datas
    instance = Post.objects.get(id=post_id)  # get comment data according to post id
    is_current_user_like = instance.like_owner.filter(username=request.user.username)
    if is_current_user_like.exists():
        instance.like_owner.remove(request.user.id)

        return HttpResponse(f'{instance.like_owner.count()}')
    else:
        instance.like_owner.add(request.user.id)
        return HttpResponse(f'{instance.like_owner.count()}')

# comment like action
def comment_like(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    is_like = comment.like_owner.filter(username=request.user.username)
    if is_like.exists():
        comment.like_owner.remove(request.user.id)
        return HttpResponse(f"<i class='fa-regular fa-heart action-icon m-812' "
                            f"style='margin:0;float:right;' "
                            f"id='likeIcon-{comment.id}'></i>")
    else:
        comment.like_owner.add(request.user.id)
        return HttpResponse(
            f"<i class='fa-solid fa-heart m-812' style='color: #e73c04; font-size:20px; margin:0;float:right;' "
            f"id='likeIcon-{comment.id}'></i> ")


def comment_like_control(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(id=request.user.id)
    # get like owners of comment
    owners = list(comment.like_owner.all())
    like_owner_list = []
    for owner in owners:
        like_owner_list.append(owner.username)

    control = like_owner_list.__contains__(user.username)
    if control:
        return HttpResponse(f"<i class='fa-solid fa-heart m-812' style='color: #e73c04; font-size:20px; margin:0;float:right;' "
                            f"id='likeIcon-{comment.id}'></i> ")
    else:
        return HttpResponse(f"<i class='fa-regular fa-heart action-icon m-812' "
                            f"style='margin:0;float:right;' "
                            f"id='likeIcon-{comment.id}'></i>")


# like control function
def like_control(request, post_id, user_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=user_id)
    # get like owners of post
    owners = list(post.like_owner.all())
    like_owner_list = []
    for owner in owners:
        like_owner_list.append(owner.username)

    control = like_owner_list.__contains__(user.username)
    if control:
        return HttpResponse(f"<i class='fa-solid fa-heart' style='color: #e73c04; font-size:20px; margin:0;' "
                            f"id='likeIcon-{post.id}'></i> ")
    else:
        return HttpResponse(f"<i class='fa-regular fa-heart action-icon' style='margin:0;' id='likeIcon-{post.id}'></i>")


def follow(request, current_user_id, target_user_id):
    # cu = current user
    # tu = target user
    # ua_cu = user action current user / ua_tu = user action target user
    cu = User.objects.get(id=current_user_id)  # get current user
    tu = User.objects.get(id=target_user_id)  # get target user
    cu.following.add(target_user_id)  # add the target user from the current user following list.
    tu.follower.add(current_user_id)  # add the current user from the target user follower list
    return redirect(f'/user/{tu.username}')


def unfollow(request, current_user_id, target_user_id):
    # cu = current user
    # tu = target user
    # ua_cu = user action current user / ua_tu = user action target user
    cu = User.objects.get(id=current_user_id)  # get current user
    tu = User.objects.get(id=target_user_id)   # get target user
    cu.following.remove(target_user_id)        # remove the target user in the current user following list.
    tu.follower.remove(current_user_id)        # remove the current user in the target user follower list.
    return redirect(f'/user/{tu.username}')

