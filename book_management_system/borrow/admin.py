from django.contrib import admin
from .models import BorrowRecord, Reservation


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'renewal_count']
    list_filter = ['status', 'borrow_date', 'due_date']
    search_fields = ['user__username', 'book__title']
    date_hierarchy = 'borrow_date'
    list_editable = ['status']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'reservation_date', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__username', 'book__title']
    date_hierarchy = 'reservation_date'
