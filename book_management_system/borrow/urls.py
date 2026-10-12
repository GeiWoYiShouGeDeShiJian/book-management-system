from django.urls import path
from . import views

app_name = 'borrow'

urlpatterns = [
    # 用户借阅功能
    path('borrow/<int:book_pk>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_pk>/', views.return_book, name='return_book'),
    path('renew/<int:borrow_pk>/', views.renew_book, name='renew_book'),
    
    # 预约功能
    path('reserve/<int:book_pk>/', views.reserve_book, name='reserve_book'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/<int:reservation_pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # 管理员功能
    path('records/', views.borrow_record_list, name='borrow_record_list'),
    path('overdue/', views.overdue_list, name='overdue_list'),
    path('admin-return/<int:borrow_pk>/', views.admin_return_book, name='admin_return_book'),
]
