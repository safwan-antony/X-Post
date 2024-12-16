from django.shortcuts import render , redirect
from .models import MessageChat  , GroopRooms , RoomChat
from a_users.models import User
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def message_chat(request , pk):
    sender = User.objects.get(id = pk)
    receiver = User.objects.get(username = request.user.username)
   
    message_chat = MessageChat.objects.filter(host = sender , friend_chat=receiver ) | MessageChat.objects.filter(host=receiver , friend_chat = sender)
    if request.method =='POST':
        message  =request.POST.get('message')
        message_chat = MessageChat.objects.create(host = receiver, friend_chat = sender , message = message )
    
        message_chat.save()
        
        
        return redirect('message_chat' , pk = sender.id) 
    context = {
       'message_chat':message_chat,
    
   
    }
    return render(request, 'chat/message_chat.html',context)

def groop_rooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    groop_rooms = GroopRooms.objects.filter(
        Q(name__icontains =q )|
        Q(slug__icontains =q )
    ) 
    rooms_count=groop_rooms.count()
    context = {
        'groop_rooms':groop_rooms,
        'rooms_count':rooms_count,
    }
    return render(request, 'chat/groop_rooms.html' , context)

def create_room(request):
    if request.method =='POST':
        room_name = request.POST.get('room_name')
        room_slug=request.POST.get('room_slug')
        if GroopRooms.objects.filter(slug = room_slug).exists():
            messages.error(request, 'This Room is Already Exists')
            return redirect('home')
        else:
            groop_rooms = GroopRooms.objects.create( owner = request.user ,name = room_name , slug = room_slug)
            groop_rooms.save()
            messages.success(request, 'Gongradulation your Room was Created Successfully')
            return redirect('home')
    
    return render(request, 'chat/create_room.html')

def room_chat(request , slug):
    room = GroopRooms.objects.get(slug = slug)
    chat = RoomChat.objects.filter(room = room)
    context = {
        'room':room,
        'chat':chat,
        'slug':slug,
}   
    return render(request, 'chat/room_chat.html' , context)

