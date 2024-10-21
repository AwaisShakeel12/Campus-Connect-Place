from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import  auth
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .forms import ChatMessageForm, AddFriendForm
from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required
# Create your views here.



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        re_enter_password = request.POST['password1']
        email = request.POST['email']
        
        role = request.POST['role']

        image = request.FILES.get('image')

        if password == re_enter_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exsist')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exsist')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password, role=role, image=image)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                
                auth.login(request, user_login)
                return redirect('home')
                

        
        else:
            messages.info(request, 'invalid data')
            return redirect('signup')



    return render(request, 'app/signup.html')


def login(request):

    
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
          
        else:
            messages.info(request, 'username or password not correct')
            return redirect('login')

    

    return render(request, 'app/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    newss = News.objects.all()
    users = User.objects.all()
    context = {"newss":newss, 'users':users}

    return render(request, 'app/home.html',context)



def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            friend = form.cleaned_data['friend_username']
            # Create a Friend instance for the selected user
            friend_profile, created = Friend.objects.get_or_create(profile=friend)
            # Add the friend to the current user's friends list
            request.user.friends.add(friend_profile)
            return redirect('add_friend')
    else:
        form = AddFriendForm()
    return render(request, 'app/add_friend.html', {'form': form})

def chat(request):
    
    users = User.objects.all()
    
    context = {'users':users}


    return render(request, 'app/chat.html', context)

def chatpage(request, pk):
    user = request.user
    friend = Friend.objects.get(profile_id=pk)
    profile = User.objects.get(pk=friend.profile.id)
    chats = ChatMessage.objects.all()
    re_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
    re_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect('chatpage', pk=friend.profile.id)



    context = {'user':user, 
            #    'friend':friend, 
               'profile':profile,
               'chats':chats,
               'form':form,
               }
    return render(request, 'app/chatpage.html', context)





def detail(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user
    profile = User.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    form = ChatMessageForm()

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect('detail', pk=friend.profile.id)
        

    context ={'friend':friend, 'form':form, 'user':user, 'profile':profile, 'chats':chats}
    return render(request, 'app/details1.html', context)


def sentMessages(request, pk):
    user = request.user
    friend = Friend.objects.get(profile_id = pk)
    profile = User.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    user = request.user
    friend = Friend.objects.get(profile_id = pk)
    profile = User.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender = profile, msg_receiver=user )
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


def event(request):
    events = Event.objects.all()
    context ={'events':events}
    return render(request, 'app/event.html', context)

def complain(request):
    complains = Complain.objects.all()
    if request.method == "POST":
        user = request.user      
        title = request.POST['title']
        description = request.POST['description']
        complain = Complain.objects.create(user=user, title=title, description=description)
        complain.save()
        return redirect('complain')
    context = {'complains':complains}
    return render(request, 'app/complain.html', context)



def books(request):
    books = Books.objects.all()
    if request.method == "POST":
        user = request.user      
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')
        books = Books.objects.create(user=user, title=title, description=description, file=file)
        books.save()
        return redirect('books')
    context = {'books':books}
    return render(request, 'app/books.html', context)


# def discussion(request):

#     discussions = CommunityForm.objects.all()
#     if request.method == "POST":
#         user = request.user
#         msg = request.POST['msg']
#         image = request.FILES.get('image')

#         discussion_forum = CommunityForm.objects.create(user=user, msg=msg, image=image)
#         discussion_forum.save()
#         return redirect('discussion')
#     context = {'discussions':discussions}
    
  
        
    # return render(request, 'app/discussion.html', context)



def profile(request, pk):
    user = User.objects.get(id=pk)
    complains = Complain.objects.all()
    books = Books.objects.all()
    context = {'user':user, 'complains':complains, 'books':books}
    return render(request, 'app/profile.html', context)

def addnews(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')

        createNews = News.objects.create(title=title, description=description, image=image)
        createNews.save()
        return redirect('addnews')

    return render(request, 'app/add_news.html')

def addevent(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        image = request.FILES.get('image')

        createEvent = Event.objects.create(title=title, description=description, date=date,image=image)
        createEvent.save()
        return redirect('addevent')


    return render(request, 'app/add_event.html')