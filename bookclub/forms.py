from django import forms
from datetime import timedelta
from .models import Book, BookReview, Borrow


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['contributor']


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['contributor']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['contributor']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_to_return = instance.date_borrowed + timedelta(days=14)
        if commit:
            instance.save()
        return instance
