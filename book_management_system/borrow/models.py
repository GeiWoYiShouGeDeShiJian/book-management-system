from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class BorrowRecord(models.Model):
    """借阅记录模型"""
    STATUS_CHOICES = [
        ('borrowed', '借出'),
        ('returned', '已归还'),
        ('overdue', '逾期'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='borrow_records'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        verbose_name='图书',
        related_name='borrowrecord'
    )
    borrow_date = models.DateTimeField('借阅日期', auto_now_add=True)
    due_date = models.DateTimeField('应还日期')
    return_date = models.DateTimeField('实际归还日期', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='borrowed')
    renewal_count = models.PositiveIntegerField('续借次数', default=0)
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '借阅记录'
        verbose_name_plural = '借阅记录'
        ordering = ['-borrow_date']

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    def save(self, *args, **kwargs):
        """保存时自动设置应还日期和状态"""
        if not self.due_date:
            # 默认借阅期限为30天
            self.due_date = timezone.now() + timedelta(days=30)
        
        # 检查是否逾期
        if self.status == 'borrowed' and self.due_date < timezone.now():
            self.status = 'overdue'
        
        super().save(*args, **kwargs)

    def is_overdue(self):
        """检查是否逾期"""
        return self.status == 'borrowed' and self.due_date < timezone.now()

    def get_days_remaining(self):
        """获取剩余天数"""
        if self.status != 'borrowed':
            return 0
        delta = self.due_date - timezone.now()
        return delta.days

    def can_renew(self):
        """检查是否可以续借"""
        # 最多续借2次，且不能逾期
        return (
            self.status == 'borrowed' and
            self.renewal_count < 2 and
            not self.is_overdue()
        )

    def renew(self):
        """续借图书"""
        if self.can_renew():
            self.due_date = self.due_date + timedelta(days=30)
            self.renewal_count += 1
            self.save()
            return True
        return False

    def return_book(self):
        """归还图书"""
        if self.status == 'borrowed':
            self.status = 'returned'
            self.return_date = timezone.now()
            self.save()
            
            # 更新图书可用册数
            self.book.available_copies += 1
            if self.book.available_copies > 0:
                self.book.status = 'available'
            self.book.save()
            return True
        return False


class Reservation(models.Model):
    """预约记录模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('fulfilled', '已完成'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='reservations'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        verbose_name='图书',
        related_name='reservations'
    )
    reservation_date = models.DateTimeField('预约日期', auto_now_add=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'
        ordering = ['-reservation_date']

    def __str__(self):
        return f'{self.user.username} 预约 {self.book.title}'
