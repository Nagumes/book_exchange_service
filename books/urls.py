from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-books/', views.my_books, name='my_books'),
    path('add/', views.add_book, name='add_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('chat/start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('my_chats/', views.my_chats, name='my_chats'),
]
