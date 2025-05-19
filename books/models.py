from django.db import models
from django.contrib.auth.models import User

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


# Модель запроса обмена книгами (если нужна)
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


