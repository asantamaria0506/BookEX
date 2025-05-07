from django import forms
from django.forms import ModelForm
from .models import Book, Comment


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search Books', max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']