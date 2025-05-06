from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('books/', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('my-books/', views.my_books, name='my_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
