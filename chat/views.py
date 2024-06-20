from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import MessageForm
from .models import Chat, Message, Profile
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_list(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    request.user.profile.online = True
    request.user.profile.last_seen = timezone.now()
    request.user.profile.save()

    chats = Chat.objects.filter(participants=request.user)
    search_query = request.GET.get('q')
    search_results = None
    if search_query:
        search_results = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {'chats': chats, 'search_results': search_results})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in chat.participants.all():
        return redirect('chat_list')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = chat.participants.exclude(id=request.user.id).first()
            message.chat = chat
            message.save()
    else:
        form = MessageForm()

    messages = Message.objects.filter(chat=chat)
    other_participant = chat.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'other_participant': other_participant,
        'form': form
    })
@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('chat_list')
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.set([request.user, other_user])
        chat.save()

    return redirect('chat_detail', chat_id=chat.id)
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_logout(request):
    request.user.profile.online = False
    request.user.profile.save()
    logout(request)
    return redirect('home')


