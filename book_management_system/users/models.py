from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户扩展资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    phone = models.CharField('手机号', max_length=20, blank=True)
    address = models.CharField('地址', max_length=200, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username} 的资料'
