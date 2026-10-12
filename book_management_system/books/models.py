from django.db import models
from django.urls import reverse


class Category(models.Model):
    """图书分类模型"""
    name = models.CharField('分类名称', max_length=100, unique=True)
    description = models.TextField('分类描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:category_detail', kwargs={'pk': self.pk})


class Author(models.Model):
    """作者模型"""
    name = models.CharField('作者姓名', max_length=100)
    biography = models.TextField('作者简介', blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:author_detail', kwargs={'pk': self.pk})


class Book(models.Model):
    """图书模型"""
    STATUS_CHOICES = [
        ('available', '可借阅'),
        ('borrowed', '已借出'),
        ('reserved', '已预约'),
        ('maintenance', '维护中'),
    ]

    title = models.CharField('书名', max_length=200)
    isbn = models.CharField('ISBN', max_length=13, unique=True, blank=True, null=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='作者',
        related_name='books'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='分类',
        related_name='books'
    )
    publisher = models.CharField('出版社', max_length=200, blank=True)
    publication_date = models.DateField('出版日期', null=True, blank=True)
    total_copies = models.PositiveIntegerField('总册数', default=1)
    available_copies = models.PositiveIntegerField('可用册数', default=1)
    description = models.TextField('描述', blank=True)
    cover_image = models.ImageField('封面图片', upload_to='book_covers/', blank=True, null=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """保存时自动更新状态"""
        if self.available_copies == 0:
            self.status = 'borrowed'
        elif self.available_copies > 0 and self.status == 'borrowed':
            self.status = 'available'
        super().save(*args, **kwargs)

    def is_available(self):
        """检查图书是否可借阅"""
        return self.available_copies > 0

    def get_borrow_count(self):
        """获取图书被借阅次数"""
        from borrow.models import BorrowRecord
        return BorrowRecord.objects.filter(book=self).count()
