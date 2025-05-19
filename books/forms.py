from django import forms
from .models import Profile, Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'genre', 'cover']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']  # Включаем аватар и никнейм
