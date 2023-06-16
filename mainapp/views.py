from django.shortcuts import render, redirect, get_object_or_404
from accountapplication.models import User, Post, Comment, Profile, Notification, Message
from . forms import CreatePost, CreateComment
from accountapplication.forms import ProfileEditForm, MessageForm
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError  # checking error
from itertools import chain  # we convert queryset with list
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.



# home page rendering
# define a try except block because if user didn't log in, we get an error about user not exist
# if user exist, get user's followers id as list. And send to home html with context.
@login_required
def home(request):
    try:
        current_user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(id=current_user.id)
        user_following_list = []
        post = []

        # get the current user following list ( if ylrmali follow -> yigitali -> it will be in list)
        # define a for loop for append all users id in list.
        # user_following = Profile.objects.filter(follower=current_user.id)
        try:
            user_following = Profile.objects.get(user=current_user.id).get_following();
            for users in user_following:
                user_following_list.append(users.id)

            # get users id in user following list.
            # get these user's post.
            # append these posts in post array
            for user_id in user_following_list:
                post_list = Post.objects.filter(owner_id=user_id)
                post.append(post_list)

            posts = list(chain(*post))  # convert queryset to list

            datas = []

            for post in posts:
                data = []
                data.append(post)
                data.append(Profile.objects.get(user=post.owner.id))
                datas.append(data)

            is_liked_list = []
            for post in posts:
                is_liked = (list(post.like_owner.all()).__contains__(request.user))
                is_liked_list.append(is_liked)


            context = {
                'current_user': profile,
                'posts': datas,
                'is_liked': is_liked_list,
            }
            return render(request, 'mainapp/home.html', context)
        except Profile.DoesNotExist:
            return HttpResponse('kullanıcı profili bulunamadi')
    except User.DoesNotExist:
        return render(request, 'mainapp/home.html')


# when user want to create new post, this function will be work
# first check request.method, if method is post -> define a try except block
@login_required
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
@login_required
def explore(request):
    post_datas = []
    posts = list(Post.objects.filter(is_active=True))
    for post in posts:
        profile = Profile.objects.get(user=post.owner)
        comments_count = Comment.objects.filter(post=post.id).count()
        datas = []
        datas.append(profile)
        datas.append(post)
        datas.append(comments_count)
        post_datas.append(datas)

    print(post_datas)
    context = {
        'post_datas': post_datas
    }
    return render(request, 'mainapp/explore.html', context)


#
@login_required 
def post_detail(request, pk):
    ''' post detail page. I get slug params in url. Check the url.py post-detail function 
        if method is post its means someone commit a comment
        else return create comment form, post, post_owner, comments_data(user profile & comment),
            comment counts.
    '''

    if request.method == 'POST':
        form = request.POST['comment_text']
        owner = request.user
        post = Post.objects.get(id=pk)
        tu_profile = Profile.objects.get(user=post.owner_id)
        user = User.objects.get(id=tu_profile.user.id)
        cu_profile = Profile.objects.get(user=owner.id)
        print(cu_profile)
        print(user)
        comment = Comment.objects.create(comment_text=form, owner=owner, post_id=post.id)
        comment.save()
        notification = Notification.objects.create(user=user, type=False,
                                                   owner_user=cu_profile,
                                                   notification={"message": f"{cu_profile.user} fotoğrafına bir yorum yaptı", 
                                                                "time": f"{datetime.now()}"},
                                                    post_id=post)
        notification.save()
        return redirect(f'/post/{pk}')
    else:
        form = CreateComment()
        post = Post.objects.get(id=pk)
        detail_datas = []
        post_owner = Profile.objects.get(user=post.owner)
        comments = list(Comment.objects.order_by('created_time').filter(post_id=pk))
        for index, comment in enumerate(comments):
            ''' get comments from comment object filtered as post id  
                get comment owner profile object filtered as user 
                then append these datas to comment_data list
                finally append this list to detail_datas list
            '''
            comment_data = []
            comment_user_photo = Profile.objects.get(user=comment.owner)
            comment_data.append(comment)
            comment_data.append(comment_user_photo)
            detail_datas.append(comment_data)

        comments_count = Comment.objects.filter(post_id=pk).count()
        context = {
            'post': post,
            'post_owner': post_owner,
            'comments_data': detail_datas,
            'comments_count': comments_count,
            'form': form,
        }
        return render(request, 'mainapp/post-detail.html', context)


# post create function
@login_required
def post_create(request):
    form = CreatePost()
    comment_id = request.GET.get('data-comment-id')
    context = {
        'form': form,
    }
    return render(request, 'mainapp/post-create.html', context)

@login_required
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
@login_required
def like(request,  post_id):
    # checking and getting old liker datas
    instance = Post.objects.get(id=post_id)  # get comment data according to post id
    user = User.objects.get(id=instance.owner_id)
    cu_profile = Profile.objects.get(user=request.user.id)
    is_current_user_like = instance.like_owner.filter(username=request.user.username)
    if is_current_user_like.exists():
        instance.like_owner.remove(request.user.id)
        notification = Notification.objects.filter(owner_user=cu_profile, post_id=instance)
        notification.delete()
        return HttpResponse(f'{instance.like_owner.count()}')
    else:
        instance.like_owner.add(request.user.id)
        notification = Notification.objects.create(user=user, type=False,
                                                   owner_user=cu_profile,
                                                   notification={"message": f"{cu_profile.user} bir fotoğrafını beğendi", 
                                                                "time": f"{datetime.now()}"},
                                                    post_id=instance)
        notification.save()
        return HttpResponse(f'{instance.like_owner.count()}')

# comment like action
@login_required
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

@login_required
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
        return HttpResponse('hello')
        return HttpResponse(f"<i class='fa-solid fa-heart m-812' style='color: #e73c04; font-size:20px; margin:0;float:right;' "
                            f"id='likeIcon-{comment.id}'></i> ")
    else:
        return HttpResponse('hello')
        return HttpResponse(f"<i class='fa-regular fa-heart action-icon m-812' "
                            f"style='margin:0;float:right;' "
                            f"id='likeIcon-{comment.id}'></i>")


# like control function
@login_required
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
        return HttpResponse(f"<i class='fa-solid fa-heart' data-like-control={control} style='color: #e73c04; font-size:20px; margin:0;' "
                            f"id='likeIcon'></i> ")
    else:
        return HttpResponse(f"<i class='fa-regular fa-heart action-icon' data-like-control={control} style='margin:0;color:white;' id='likeIcon'></i>")

@login_required
def follow(request, current_user_id, target_user_id):
    # cu = current user
    # tu = target user
    # ua_cu = user action current user / ua_tu = user action target user
    cu = Profile.objects.get(user=current_user_id)  # get current user
    tu = Profile.objects.get(user=target_user_id)  # get target user
    user = User.objects.get(username=tu.user)
    instance = list(Notification.objects.filter(owner_user=cu,type=True))

    if tu.is_lock:
        if instance == []:
            notification = Notification.objects.create(user=user, type=True,
                                                    owner_user=cu, 
                                                    notification={"message": f"{cu.user} kullanıcısı seni takip etmek istiyor", 
                                                                    "time": f"{datetime.now()}"})
            notification.save()
        return HttpResponse('''<p>Takip isteği gönderildi!<p>
                               <i class="fa-solid fa-xmark" onclick="document.getElementById('notification').style.display='none'"></i>
                            ''')
    else:
        if instance == []:
            notification = Notification.objects.create(user=user, type=True,
                                                    owner_user=cu,
                                                    notification={"message": f"{cu.user} kullanıcısı artık seni takip ediyor", 
                                                                    "time": f"{datetime.now()}"})
            notification.save()    
        cu.following.add(target_user_id)  # add the target user from the current user following list.
        tu.follower.add(current_user_id)  # add the current user from the target user follower list
        return redirect(f'/user/{tu.user_id}')

@login_required
def unfollow(request, current_user_id, target_user_id):
    # cu = current user
    # tu = target user
    # ua_cu = user action current user / ua_tu = user action target user
    cu = Profile.objects.get(user=current_user_id)  # get current user
    tu = Profile.objects.get(user=target_user_id)   # get target user
    cu.following.remove(target_user_id)        # remove the target user in the current user following list.
    tu.follower.remove(current_user_id)        # remove the current user in the target user follower list.
    notification = Notification.objects.filter(user_id=tu.id, type=True)
    notification.delete()
    return redirect(f'/user/{tu.user_id}')

@login_required
def accept_follower(request, current_user_id, target_user_id, noti_id):
    cu = Profile.objects.get(user=current_user_id)  # get current user
    tu = Profile.objects.get(user=target_user_id)  # get target user
    user = User.objects.get(username=tu.user)
    cu.follower.add(target_user_id)  # add the target user from the current user following list.
    tu.following.add(current_user_id)  # add the current user from the target user follower list
    notification = Notification.objects.get(id=noti_id)
    notification.is_read = True
    notification.save()
    re_notification = Notification.objects.create(user=user, type=False,
                                                    owner_user=cu, 
                                                    notification={"message": f"{cu.user} kullanıcısı takip isteğini kabul etti", 
                                                                    "time": f"{datetime.now()}"})
    re_notification.save()
    return HttpResponse("Onayla")

@login_required
def ignore_follower(request, noti_id):
    ''' when user click the ignore button in following notification this function will be run '''
    notification = Notification.objects.get(id=noti_id)
    notification.delete()
    return HttpResponse("Reddet")    


@login_required
def refollow(request, current_user_id, target_user_id, noti_id):
    follow(request, current_user_id, target_user_id)
    notification = Notification.objects.get(id=noti_id)
    notification.delete()
    return HttpResponse('Geri Takip Et')


@login_required
def search(request, argument):
    ''' this function search user when user type something in search bar '''
    user = User.objects.filter(username__contains=argument)
    ''' get users profile photos '''
    user_list = list(user)
    user_datas = []
    for index, u in enumerate(user):
        photo = Profile.objects.get(user=u.id).profile_photo
        print(index, u, type(user_list[index]))
        item = []
        item.append(u)
        item.append(str(photo))
        user_datas.append(item)
    context = {
        'users': user_datas,
    }
    
    return render(request, 'mainapp/search_list.html', context)


@login_required
def profile_edit(request, user_id):
    ''' 
        edit user profile with this function
        this function works with django forms 
        this function can update user profile photo and background photo
    '''
    if request.method == 'POST':
        instance = Profile.objects.get(user=user_id)
        form = ProfileEditForm(request.FILES, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(f'/user/{user_id}')
        
    else:
        form = ProfileEditForm()
        context = {
            'form': form
        }
        return render(request, 'accountapplication/partials/_edit_profile.html', context)
    

@login_required
def notification(request):
    notifications = list(Notification.objects.filter(user=request.user).order_by('-id'))
    profile = Profile.objects.get(user=request.user)
    context = {
        'notifications': notifications,
        'profile': profile
    }
    return render(request, 'mainapp/notification.html', context)


@login_required
def message(request, sender, reciever):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            input_value = form.cleaned_data['content']
            reciever_profile = Profile.objects.get(id=reciever)
            sender_profile = Profile.objects.get(id=sender)
            message = form.save(commit=False)  # Get the model instance without saving to the database
            message.reciever = reciever_profile
            message.sender = sender_profile
            message.save()
            return redirect(request.path_info)
    else:
        if sender != request.user.id:
            raise Http404("Page not found")
        else:
            try:
                sender = Profile.objects.get(id=sender)
                reciever = Profile.objects.get(id=reciever)
                form = MessageForm
                messages = Message.objects.filter(
                    Q(reciever=sender, sender=reciever) | Q(reciever=reciever, sender=sender)
                    ).order_by('timestamp')
                context = {
                    'sender': sender,
                    'reciever': reciever,
                    'form': form,
                    'messages': messages
                }
                return render(request, 'mainapp/message.html', context)
            except:
                raise Http404("Page not found")


@login_required
def message_box(request, current_user):
    if current_user != request.user.id:
        raise Http404("Page not found")
    else:
        messages = list(Message.objects.filter(Q(reciever=current_user) | Q(sender=current_user)))
        all_ids = []
        for msg in messages:
            all_ids.append(msg.sender.id)
            all_ids.append(msg.reciever.id)

        filtered_ids = list(set(all_ids))
        profiles = []
        current_user_profile = ''

        for id in filtered_ids:
            profile = Profile.objects.get(id=id)
            if id != current_user:
                profiles.append(profile)
            else:
                current_user_profile = profile    

        context = {
            'profiles': profiles,
            'current_user': current_user_profile,
        }
        return render(request, 'mainapp/message-box.html', context)