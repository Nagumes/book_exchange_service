from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import BookForm, ProfileForm
from .models import Book, Profile

# Страница регистрации
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Страница входа
def login_view(request):
    return render(request, 'registration/login.html')

# Страница выхода
def logout_view(request):
    logout(request)
    return redirect('login')

# Мои книги
@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user)
    return render(request, 'books/my_books.html', {'books': books})

# Добавить книгу
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# Редактировать книгу
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user != book.owner and not request.user.is_staff:
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

# Удалить книгу
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user != book.owner and not request.user.is_staff:
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'books/confirm_delete.html', {'book': book})

# Редактировать профиль
@login_required
def edit_profile(request):
    # Пытаемся получить профиль, если нет — создаём
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_books')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'books/edit_profile.html', {'form': form})

# Список всех книг с поиском и фильтрацией по жанру
def book_list(request):
    # Получаем параметры из строки запроса
    query = request.GET.get('search', '').strip()
    selected_genre = request.GET.get('genre', '')

    # Все книги
    books = Book.objects.all()

    # Поиск по названию или автору
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # Фильтрация по жанру
    if selected_genre:
        books = books.filter(genre=selected_genre)

    # Получаем список всех жанров из модели Book
    genre_choices = [choice[0] for choice in Book._meta.get_field('genre').choices if choice[0]]

    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genre_choices,
        'selected_genre': selected_genre,
        'query': query,
    })


# Детали книги
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})
