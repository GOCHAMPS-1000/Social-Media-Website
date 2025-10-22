# social_media/core/views.py
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Follow, Like, Comment, Notification
from .forms import PostForm, AccountSettingsForm

def home(request):
    if request.user.is_authenticated:
        return redirect('post_feed')
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_feed')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_feed')
    else:
        form = AuthenticationForm()
    return render(request, 'core/signin.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('signin')

@login_required
def account_settings(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = AccountSettingsForm(instance=request.user)
    return render(request, 'core/account_settings.html', {'form': form})

@login_required
def upload_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_feed')
    else:
        form = PostForm()
    return render(request, 'core/upload_post.html', {'form': form})

@login_required
def post_feed(request):
    # Get posts from users that the current user follows
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-created_at') | Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/post_feed.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        liked = False
    else:
        # Create notification for the post owner
        if request.user != post.user:
            Notification.objects.create(
                user=post.user, 
                message=f"{request.user.username} liked your post."
            )
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_set.count()
        })
    
    return redirect('post_feed')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    # Get counts
    post_count = posts.count()
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    return render(request, 'core/profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(
            follower=request.user, 
            following=user_to_follow
        )
        
        if created:
            # Create notification for the user being followed
            Notification.objects.create(
                user=user_to_follow, 
                message=f"{request.user.username} started following you."
            )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'following': True,
            'follower_count': Follow.objects.filter(following=user_to_follow).count()
        })
    
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'following': False,
            'follower_count': Follow.objects.filter(following=user_to_unfollow).count()
        })
    
    return redirect('profile', username=username)

@login_required
def search_user(request):
    query = request.GET.get('q')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'core/search_user.html', {'users': users, 'query': query})

@login_required
def user_suggestions(request):
    # Get users not followed by the current user
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    suggestions = User.objects.exclude(id__in=following).exclude(id=request.user.id)[:5]
    return render(request, 'core/user_suggestions.html', {'suggestions': suggestions})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        
        # Create notification for the post owner
        if request.user != post.user:
            Notification.objects.create(
                user=post.user, 
                message=f"{request.user.username} commented on your post."
            )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'content': comment.content,
                    'user': comment.user.username,
                    'created_at': comment.created_at.strftime('%b. %d, %Y, %I:%M %p')
                }
            })
    
    return redirect('post_feed')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': user_notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications')