from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Модель книги
class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-fiction'),
        ('mystery', 'Mystery'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('poetry', 'Poetry'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField(null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')  # 🔹 новое поле
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Модель запроса обмена книгами
class ExchangeRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Книга для обмена
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')  # Запрашивающий книгу
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')  # Статус запроса

    def __str__(self):
        return f"Request for {self.book.title} by {self.requester.username}"

# Модель профиля
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, null=True)  # Никнейм
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Аватарка

    def __str__(self):
        return self.user.username



class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} ({', '.join(p.username for p in self.participants.all())})"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']


User = get_user_model()

class ChatUserStatus(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('chat', 'user')

    def __str__(self):
        return f'{self.user.username} status in chat {self.chat.id}'

