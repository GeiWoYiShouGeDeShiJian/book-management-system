from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import BorrowRecord, Reservation
from .forms import BorrowForm, ReturnForm, ReservationForm, RenewForm
from books.models import Book


def is_admin(user):
    """检查用户是否为管理员"""
    return user.is_staff


@login_required
def borrow_book(request, book_pk):
    """借阅图书视图"""
    book = get_object_or_404(Book, pk=book_pk)
    
    # 检查图书是否可借阅
    if not book.is_available():
        messages.error(request, '该图书暂无可借阅的副本！')
        return redirect('books:book_detail', pk=book_pk)
    
    # 检查用户是否已借阅该图书
    existing_borrow = BorrowRecord.objects.filter(
        book=book,
        user=request.user,
        status='borrowed'
    ).first()
    
    if existing_borrow:
        messages.warning(request, '您已经借阅了这本图书！')
        return redirect('books:book_detail', pk=book_pk)
    
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            # 创建借阅记录
            borrow_record = form.save(commit=False)
            borrow_record.user = request.user
            borrow_record.book = book
            borrow_record.due_date = timezone.now() + timedelta(days=30)
            borrow_record.save()
            
            # 更新图书可用册数
            book.available_copies -= 1
            if book.available_copies == 0:
                book.status = 'borrowed'
            book.save()
            
            messages.success(
                request, 
                f'成功借阅《{book.title}》！请在 {borrow_record.due_date.strftime("%Y-%m-%d")} 前归还。'
            )
            return redirect('users:borrow_history')
    else:
        form = BorrowForm()
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'borrow/borrow_form.html', context)


@login_required
def return_book(request, borrow_pk):
    """归还图书视图"""
    borrow_record = get_object_or_404(BorrowRecord, pk=borrow_pk, user=request.user)
    
    if borrow_record.status != 'borrowed':
        messages.warning(request, '该图书已经归还！')
        return redirect('users:borrow_history')
    
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            # 归还图书
            borrow_record.return_book()
            messages.success(request, f'成功归还《{borrow_record.book.title}》！')
            return redirect('users:borrow_history')
    else:
        form = ReturnForm()
    
    context = {
        'form': form,
        'borrow_record': borrow_record,
    }
    return render(request, 'borrow/return_form.html', context)


@login_required
def renew_book(request, borrow_pk):
    """续借图书视图"""
    borrow_record = get_object_or_404(BorrowRecord, pk=borrow_pk, user=request.user)
    
    if not borrow_record.can_renew():
        messages.error(request, '该图书无法续借！可能已达到续借上限或已逾期。')
        return redirect('users:borrow_history')
    
    if request.method == 'POST':
        form = RenewForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            if borrow_record.renew():
                messages.success(
                    request, 
                    f'成功续借《{borrow_record.book.title}》！新的应还日期为 {borrow_record.due_date.strftime("%Y-%m-%d")}。'
                )
            else:
                messages.error(request, '续借失败！')
            return redirect('users:borrow_history')
    else:
        form = RenewForm()
    
    context = {
        'form': form,
        'borrow_record': borrow_record,
    }
    return render(request, 'borrow/renew_form.html', context)


@login_required
def reserve_book(request, book_pk):
    """预约图书视图"""
    book = get_object_or_404(Book, pk=book_pk)
    
    # 检查图书是否可预约（已借出但有人预约）
    if book.is_available():
        messages.info(request, '该图书目前可借阅，请直接借阅！')
        return redirect('books:book_detail', pk=book_pk)
    
    # 检查用户是否已预约
    existing_reservation = Reservation.objects.filter(
        book=book,
        user=request.user,
        status='pending'
    ).first()
    
    if existing_reservation:
        messages.warning(request, '您已经预约了这本图书！')
        return redirect('books:book_detail', pk=book_pk)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.book = book
            reservation.save()
            
            messages.success(request, f'成功预约《{book.title}》！图书可用时我们会通知您。')
            return redirect('borrow:reservation_list')
    else:
        form = ReservationForm()
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'borrow/reservation_form.html', context)


@login_required
def reservation_list(request):
    """预约列表视图"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'borrow/reservation_list.html', {'page_obj': page_obj})


@login_required
def cancel_reservation(request, reservation_pk):
    """取消预约视图"""
    reservation = get_object_or_404(Reservation, pk=reservation_pk, user=request.user)
    
    if reservation.status != 'pending':
        messages.warning(request, '该预约无法取消！')
        return redirect('borrow:reservation_list')
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f'已取消预约《{reservation.book.title}》！')
        return redirect('borrow:reservation_list')
    
    return render(request, 'borrow/cancel_reservation.html', {'reservation': reservation})


@login_required
@user_passes_test(is_admin)
def borrow_record_list(request):
    """借阅记录列表视图（管理员）"""
    records = BorrowRecord.objects.all().select_related('user', 'book').order_by('-borrow_date')
    
    # 搜索和筛选
    status = request.GET.get('status')
    keyword = request.GET.get('keyword')
    
    if status:
        records = records.filter(status=status)
    if keyword:
        records = records.filter(
            Q(user__username__icontains=keyword) |
            Q(book__title__icontains=keyword)
        )
    
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': BorrowRecord.STATUS_CHOICES,
    }
    return render(request, 'borrow/borrow_record_list.html', context)


@login_required
@user_passes_test(is_admin)
def overdue_list(request):
    """逾期列表视图（管理员）"""
    overdue_records = BorrowRecord.objects.filter(
        status='borrowed',
        due_date__lt=timezone.now()
    ).select_related('user', 'book').order_by('due_date')
    
    paginator = Paginator(overdue_records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'borrow/overdue_list.html', {'page_obj': page_obj})


@login_required
@user_passes_test(is_admin)
def admin_return_book(request, borrow_pk):
    """管理员归还图书视图"""
    borrow_record = get_object_or_404(BorrowRecord, pk=borrow_pk)
    
    if borrow_record.status != 'borrowed':
        messages.warning(request, '该图书已经归还！')
        return redirect('borrow:borrow_record_list')
    
    if request.method == 'POST':
        borrow_record.return_book()
        messages.success(request, f'成功为 {borrow_record.user.username} 归还《{borrow_record.book.title}》！')
        return redirect('borrow:borrow_record_list')
    
    return render(request, 'borrow/admin_return_confirm.html', {'borrow_record': borrow_record})
