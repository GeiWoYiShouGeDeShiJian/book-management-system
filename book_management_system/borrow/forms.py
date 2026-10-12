from django import forms
from .models import BorrowRecord, Reservation


class BorrowForm(forms.ModelForm):
    """借阅表单"""
    class Meta:
        model = BorrowRecord
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReturnForm(forms.Form):
    """归还表单"""
    notes = forms.CharField(
        label='备注',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


class ReservationForm(forms.ModelForm):
    """预约表单"""
    class Meta:
        model = Reservation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RenewForm(forms.Form):
    """续借表单"""
    confirm = forms.BooleanField(
        label='确认续借（延长30天）',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
