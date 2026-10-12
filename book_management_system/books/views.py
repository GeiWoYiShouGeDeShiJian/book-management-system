from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Book, Category, Author
from .forms import BookForm, CategoryForm, AuthorForm, BookSearchForm
from borrow.models import BorrowRecord


def is_admin(user):
    """检查用户是否为管理员"""
    return user.is_staff


def home(request):
    """首页视图"""
    context = {
        'total_books': Book.objects.count(),
        'total_categories': Category.objects.count(),
        'total_authors': Author.objects.count(),
        'recent_books': Book.objects.all()[:6],
        'popular_books': Book.objects.annotate(
            borrow_count=Count('borrowrecord')
        ).order_by('-borrow_count')[:5],
    }
    return render(request, 'books/home.html', context)


def book_list(request):
    """图书列表视图"""
    books = Book.objects.all().select_related('author', 'category')
    
    # 搜索功能
    search_form = BookSearchForm(request.GET)
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        category = search_form.cleaned_data.get('category')
        author = search_form.cleaned_data.get('author')
        
        if keyword:
            books = books.filter(
                Q(title__icontains=keyword) |
                Q(isbn__icontains=keyword) |
                Q(author__name__icontains=keyword)
            )
        if category:
            books = books.filter(category=category)
        if author:
            books = books.filter(author=author)
    
    # 分页
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'categories': Category.objects.all(),
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """图书详情视图"""
    book = get_object_or_404(Book, pk=pk)
    
    # 获取当前用户的借阅记录
    user_borrow_record = None
    if request.user.is_authenticated:
        user_borrow_record = BorrowRecord.objects.filter(
            book=book,
            user=request.user,
            status='borrowed'
        ).first()
    
    # 获取借阅统计
    borrow_count = BorrowRecord.objects.filter(book=book).count()
    
    context = {
        'book': book,
        'user_borrow_record': user_borrow_record,
        'borrow_count': borrow_count,
    }
    return render(request, 'books/book_detail.html', context)


@login_required
@user_passes_test(is_admin)
def book_create(request):
    """创建图书视图（管理员）"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.available_copies = book.total_copies
            book.save()
            messages.success(request, f'图书《{book.title}》创建成功！')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': '添加图书'
    })


@login_required
@user_passes_test(is_admin)
def book_update(request, pk):
    """更新图书视图（管理员）"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            # 调整可用册数
            borrowed = book.total_copies - book.available_copies
            book.available_copies = max(0, book.total_copies - borrowed)
            book.save()
            messages.success(request, f'图书《{book.title}》更新成功！')
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {
        'form': form,
        'title': '编辑图书',
        'book': book
    })


@login_required
@user_passes_test(is_admin)
def book_delete(request, pk):
    """删除图书视图（管理员）"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'图书《{title}》已删除！')
        return redirect('books:book_list')
    
    return render(request, 'books/book_confirm_delete.html', {'book': book})


def category_list(request):
    """分类列表视图"""
    categories = Category.objects.annotate(book_count=Count('books'))
    return render(request, 'books/category_list.html', {'categories': categories})


def category_detail(request, pk):
    """分类详情视图"""
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category).select_related('author')
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'books/category_detail.html', context)


@login_required
@user_passes_test(is_admin)
def category_create(request):
    """创建分类视图（管理员）"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'分类「{category.name}」创建成功！')
            return redirect('books:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'books/category_form.html', {
        'form': form,
        'title': '添加分类'
    })


@login_required
@user_passes_test(is_admin)
def category_update(request, pk):
    """更新分类视图（管理员）"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'分类「{category.name}」更新成功！')
            return redirect('books:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'books/category_form.html', {
        'form': form,
        'title': '编辑分类',
        'category': category
    })


@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    """删除分类视图（管理员）"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'分类「{name}」已删除！')
        return redirect('books:category_list')
    
    return render(request, 'books/category_confirm_delete.html', {'category': category})


def author_list(request):
    """作者列表视图"""
    authors = Author.objects.annotate(book_count=Count('books'))
    return render(request, 'books/author_list.html', {'authors': authors})


def author_detail(request, pk):
    """作者详情视图"""
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'books/author_detail.html', context)


@login_required
@user_passes_test(is_admin)
def author_create(request):
    """创建作者视图（管理员）"""
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'作者「{author.name}」创建成功！')
            return redirect('books:author_list')
    else:
        form = AuthorForm()
    
    return render(request, 'books/author_form.html', {
        'form': form,
        'title': '添加作者'
    })


@login_required
@user_passes_test(is_admin)
def author_update(request, pk):
    """更新作者视图（管理员）"""
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, f'作者「{author.name}」更新成功！')
            return redirect('books:author_list')
    else:
        form = AuthorForm(instance=author)
    
    return render(request, 'books/author_form.html', {
        'form': form,
        'title': '编辑作者',
        'author': author
    })


@login_required
@user_passes_test(is_admin)
def author_delete(request, pk):
    """删除作者视图（管理员）"""
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        name = author.name
        author.delete()
        messages.success(request, f'作者「{name}」已删除！')
        return redirect('books:author_list')
    
    return render(request, 'books/author_confirm_delete.html', {'author': author})


@login_required
@user_passes_test(is_admin)
def statistics(request):
    """统计分析视图（管理员）"""
    from django.db.models import Count, Avg
    from datetime import timedelta
    
    # 基础统计
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_authors = Author.objects.count()
    
    # 借阅统计
    total_borrows = BorrowRecord.objects.count()
    active_borrows = BorrowRecord.objects.filter(status='borrowed').count()
    overdue_borrows = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__lt=timezone.now()
    ).count()
    
    # 热门图书
    popular_books = Book.objects.annotate(
        borrow_count=Count('borrowrecord')
    ).order_by('-borrow_count')[:10]
    
    # 热门分类
    popular_categories = Category.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:10]
    
    # 最近借阅
    recent_borrows = BorrowRecord.objects.select_related(
        'book', 'user'
    ).order_by('-borrow_date')[:10]
    
    context = {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_authors': total_authors,
        'total_borrows': total_borrows,
        'active_borrows': active_borrows,
        'overdue_borrows': overdue_borrows,
        'popular_books': popular_books,
        'popular_categories': popular_categories,
        'recent_borrows': recent_borrows,
    }
    return render(request, 'books/statistics.html', context)
