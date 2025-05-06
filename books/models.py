from django.db import models
from django.contrib.auth.models import User

# Модель книги
class Book(models.Model):
    title = models.CharField(max_length=100)  # Название книги
    author = models.CharField(max_length=100)  # Автор книги
    description = models.TextField()  # Описание книги
    published_date = models.DateField(null=True, blank=True)  # Дата публикации (необязательно)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец книги (пользователь)

    def __str__(self):
        return self.title  # Возвращаем название книги как строковое представление

# Модель запроса обмена книгами (если нужна)
class ExchangeRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Книга для обмена
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')  # Запрашивающий книгу
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')  # Статус запроса

    def __str__(self):
        return f"Request for {self.book.title} by {self.requester.username}"
