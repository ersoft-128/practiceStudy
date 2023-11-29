from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from base.forms import RoomFrom
# Create your views here.




# rooms = [
#     {'id':1,"name":"lets learn python"},
#     {'id':2,"name":"Design with python"},
#     {'id':3,"name":"Make Forntend with python"},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                Q(name__icontains=q) | 
                                Q(description__icontains=q)
                                )

    topic = Topic.objects.all()

    room_count = rooms.count()

    context = {"rooms":rooms,"topic":topic,"room_count":room_count}
    return render(request,'base/home.html',context)


def room(request,pk):

    room = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = {'room': room}  
    return render(request,'base/room.html',context)


def createRoom(request):
    form = RoomFrom()

    if request.method == "POST":
       form = RoomFrom(request.POST)
       if form.is_valid():
          form.save()
          return redirect('home')

    context ={'form':form}
    return render(request,"base/create.html",context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomFrom(instance=room)

    if request.method == "POST":
        form = RoomFrom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")



    context = {'form': form}
    return render(request,"base/create.html", context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, "base/delete.html")