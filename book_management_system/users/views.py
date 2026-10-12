from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserProfileForm
from .models import UserProfile


def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 创建用户资料
            UserProfile.objects.create(user=user)
            messages.success(request, '注册成功！请登录。')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'欢迎回来，{user.first_name or username}！')
                return redirect('books:book_list')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    """用户登出视图"""
    logout(request)
    messages.info(request, '您已成功退出登录。')
    return redirect('books:book_list')


@login_required
def profile(request):
    """用户个人资料视图"""
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def user_borrow_history(request):
    """用户借阅历史视图"""
    from borrow.models import BorrowRecord
    borrow_records = BorrowRecord.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'users/borrow_history.html', {'borrow_records': borrow_records})
