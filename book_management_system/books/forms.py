from django import forms
from .models import Book, Category, Author


class BookForm(forms.ModelForm):
    """图书表单"""
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author', 'category', 'publisher', 
                  'publication_date', 'total_copies', 'description', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all().order_by('name')
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['isbn'].required = False
        self.fields['cover_image'].required = False


class CategoryForm(forms.ModelForm):
    """分类表单"""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AuthorForm(forms.ModelForm):
    """作者表单"""
    class Meta:
        model = Author
        fields = ['name', 'biography', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'birth_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
        }


class BookSearchForm(forms.Form):
    """图书搜索表单"""
    keyword = forms.CharField(
        label='关键词',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '搜索书名、作者、ISBN...'}
        )
    )
    category = forms.ModelChoiceField(
        label='分类',
        required=False,
        queryset=Category.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    author = forms.ModelChoiceField(
        label='作者',
        required=False,
        queryset=Author.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
