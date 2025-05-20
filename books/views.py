from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # Импорт модели User для чата
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import BookForm, ProfileForm
from .models import Book, Profile, Chat, Message, ChatUserStatus
from django.utils.timezone import now


# Регистрация пользователя
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books:book_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Вход
def login_view(request):
    return render(request, 'registration/login.html')

# Выход
def logout_view(request):
    logout(request)
    return redirect('books:login')

# Список книг
def book_list(request):
    query = request.GET.get('search')
    genre = request.GET.get('genre')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)
    if genre:
        books = books.filter(genre=genre)

    genres = [choice[0] for choice in Book.GENRE_CHOICES]

    return render(request, 'books/book_list.html', {
        'books': books,
        'genres': genres,
    })

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
            return redirect('books:book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# Детали книги
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

# Редактировать книгу
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user != book.owner and not request.user.is_staff:
        return redirect('books:book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

# Удалить книгу
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user != book.owner and not request.user.is_staff:
        return redirect('books:book_list')

    if request.method == 'POST':
        book.delete()
        return redirect('books:book_list')

    return render(request, 'books/confirm_delete.html', {'book': book})

# Редактировать профиль
@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('books:my_books')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'books/edit_profile.html', {'form': form})

# --- Чат ---

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user = request.user

    chat = Chat.objects.filter(participants=user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(user, other_user)
        chat.save()

    return redirect('books:chat_detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Обновляем last_read для пользователя
    status, created = ChatUserStatus.objects.get_or_create(chat=chat, user=request.user)
    status.last_read = now()
    status.save()

    messages = chat.messages.all()
    context = {'chat': chat, 'messages': messages}
    return render(request, 'books/chat_detail.html', context)

@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'books/chat_list.html', {'chats': chats})

@login_required
def send_message(request, chat_id):
    if request.method == "POST":
        chat = get_object_or_404(Chat, id=chat_id)
        if request.user not in chat.participants.all():
            return redirect('books:book_list')  # или другую страницу

        text = request.POST.get('message')
        if text:
            Message.objects.create(chat=chat, sender=request.user, content=text)
    return redirect('books:chat_detail', chat_id=chat_id)

@login_required
def my_chats(request):
    user = request.user
    chats = Chat.objects.filter(participants=user)

    chats_with_unread = []

    for chat in chats:
        try:
            status = chat.statuses.get(user=user)
            last_read = status.last_read
        except ChatUserStatus.DoesNotExist:
            last_read = None

        unread_count = chat.messages.filter(timestamp__gt=last_read).count() if last_read else chat.messages.count()

        # Получить собеседника (кроме текущего пользователя)
        other_users = chat.participants.exclude(id=user.id)
        chats_with_unread.append({
            'chat': chat,
            'unread_count': unread_count,
            'other_users': other_users,
        })

    context = {'chats_with_unread': chats_with_unread}
    return render(request, 'books/my_chats.html', context)
