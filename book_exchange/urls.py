from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Функция для автоматического редиректа с "/" на "/signup/"
def root_redirect(request):
    return redirect('signup')  # Перенаправление на страницу регистрации

urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель
    path('', root_redirect),  # 🔹 стартовая страница ведёт на /signup/
    path('books/', include('books.urls')),  # Включаем URL'ы из приложения books
    path('accounts/', include('django.contrib.auth.urls')),  # URL'ы для аутентификации Django
]
