from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('chat', views.chat, name='chat'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('chatpage/<str:pk>/', views.chatpage, name='chatpage'),
    path('detail/<str:pk>/', views.detail, name='detail'), 
    path('sent_msg/<str:pk>', views.sentMessages, name='sent_msg'), 
    path('rec_msg/<str:pk>', views.receivedMessages, name='rec_msg'), 
    path('event', views.event, name='event'),
    path('complain', views.complain, name='complain'),
    path('books', views.books, name='books'),
    path('addnews', views.addnews, name='addnews'),
    path('addevent', views.addevent, name='addevent'),
    # path('discussion', views.discussion, name='discussion'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    
]


