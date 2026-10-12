from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """用户注册表单"""
    email = forms.EmailField(
        label='邮箱',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )
    first_name = forms.CharField(
        label='姓名',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请确认密码'}
        )
        self.fields['password1'].label = '密码'
        self.fields['password2'].label = '确认密码'


class UserLoginForm(AuthenticationForm):
    """用户登录表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )


class UserUpdateForm(forms.ModelForm):
    """用户信息更新表单"""
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    """用户资料表单"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'avatar', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
