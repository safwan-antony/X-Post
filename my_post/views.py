from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from a_users.models import User
from .models import Post , Comment
from chat.models import MessageChat
from django.db.models import Q
# Create your views here.

@login_required(login_url='account_login')
def home(request):
    
    q= request.GET.get('q')  if request.GET.get('q') != None else ''
    user = User.objects.get(username=request.user.username) 
    post = Post.objects.filter(
        Q(body__icontains=q )|
        Q(user__username__icontains=q)
        )
    participants = User.objects.filter(
        Q(username__icontains=q ))
    message_chat = MessageChat.objects.all()
    message = MessageChat.objects.all() 
    
    if request.method == 'POST':
        file_p = request.FILES.get('file')
        body = request.POST.get('body')
        post = Post.objects.create(user=user, body=body , file_post=file_p)
        post.save()
        return redirect('home')
    context = {'user': user , 
               'post':post,
               'message':message,
               'message_chat':message_chat,
               'participants':participants
              
               }
    return render(request, 'my_post/home.html',context)

def comment(request , pk):
    post = Post.objects.get(id = pk)
    comment = Comment.objects.filter(post=post)
    if request.method == 'POST':
        body = request.POST.get('body')
        user = User.objects.get(username=request.user.username)
        comment = Comment.objects.create(user=user, body=body , post=post)
        comment.save()
        return redirect('comment' , pk)
    context = {'post': post ,
               'comment': comment,
               
               }
    return render(request , 'my_post/post_comment.html' , context)

def delete(request , pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        post.delete()
        return redirect('account_profile' , post.user.id)
    context = {'obj':post}
    
    return render(request , 'my_post/delete.html',context)

def delete_comment(request , pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return redirect('comment' , comment.post.id)
    context = {'obj':comment}
    
    return render(request , 'my_post/delete.html',context)

def edit_comment(request , pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment = Comment.objects.get(id=pk)
        comment.body = request.POST.get('body')
        comment.save()
        return redirect('comment' , comment.post.id)
    context = {'comment':comment}

    return render(request , 'my_post/edit_comment.html',context)

