from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('boards:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_http_methods(["POST"])
def logout(request):
    auth_logout(request)
    return redirect('boards:index')



@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
@require_http_methods(["POST"])
def follow(request, user_pk):
    me = request.user
    you = User.objects.get(pk=user_pk)
    if me != you:
        if me.followings.filter(pk=you.pk).exists():
            me.followings.remove(you)
        else:
            me.followings.add(you)

    return redirect('accounts:profile', you.username)


@login_required
def profile(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    followers = user.followers.all() # 프로필 페이지 주인의 팔로워
    followings = user.followings.all() # 프로필 페이지 주인의 팔로잉
    boards = user.board_set.all()
    comments = user.comment_set.all()
    like_boards = user.like_boards.all()

    context = {
        'user': user,
        'followers': followers,
        'followings': followings,
        'boards': boards,
        'comments': comments,
        'like_boards': like_boards,
    }
    return render(request, 'accounts/profile.html', context)