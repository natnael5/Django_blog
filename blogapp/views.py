
from .models import Post,Like
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



def post_list(request):
    posts = Post.objects.all()
    user_has_liked = {}

    if request.user.is_authenticated:
        for post in posts:
            user_has_liked[post.id] = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, 'blogapp/post_list.html', {'posts': posts, 'user_has_liked': user_has_liked})


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid login credentials.')

    return redirect('post_list')  # Redirect to post list on GET request

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('post_list')
        else:
            messages.error(request, 'Error creating account. Please check the form.')

    return redirect('post_list')  # Redirect to post list on GET request

def logout_view(request):
    logout(request)
    return redirect('post_list')

# views.py

from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    # Perform any logic to handle liking a post (e.g., add a like object to the post)
    # For simplicity, let's assume each user can like a post only once
    if post.likes.filter(id=request.user.id).exists():
        # User has already liked the post, unlike it
        post.likes.remove(request.user)
    else:
        # User hasn't liked the post, like it
        post.likes.add(request.user)
    return redirect('post_list')

@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_text = request.POST['comment']
        # Create a new comment for the post
        Comment.objects.create(post=post, author=request.user, text=comment_text)
    return redirect('post_list')