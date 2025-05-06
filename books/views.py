from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .forms import BookForm
from .models import Book
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    return redirect('book_list')

def book_list(request):
    books = Book.objects.exclude(owner=request.user) if request.user.is_authenticated else Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')  # После добавления книги редирект на список книг
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_page = request.GET.get('next', '/books/')
            return HttpResponseRedirect(next_page)  # Редирект после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user)
    return render(request, 'books/my_books.html', {'books': books})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user == book.owner or request.user.is_staff:  # Проверяем владельца или администратора
        book.delete()
    return redirect('book_list')  # После удаления перенаправляем на список книг

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})
