from django.shortcuts import render, redirect
from django.views import View
from .models import Room, RoomReservation
import datetime

class AddNewRoom(View):
    def get(self, request):
        return render(request, 'add_new_room.html')
    def post(self, request):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector_available = request.POST.get('projector_available') == "on"
        if Room.objects.filter(name=name).first():
            ctx = {
                "error": "There is already a room with this name!"
            }
            return render(request, 'add_new_room.html', ctx)
        if not name:
            ctx = {
                "error": "No name typed in!"
            }
            return render(request, 'add_new_room.html', ctx)
        if capacity <= 0:
            ctx = {
                "error": "Capacity cannot be lower than 0!"
            }
            return render(request, 'add_new_room.html', ctx)
        else:
            Room.objects.create(name=name, capacity=capacity, projector_available=projector_available)
            return redirect("room-list")

class ShowAllRooms(View):
    def get(self, request):
        rooms = Room.objects.all()
        ctx = {"rooms": rooms}
        return render(request, "show_all_rooms.html", ctx)

class DeleteRoom(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        return redirect("room-list")

class ModifyRoom(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        ctx = {"room": room}
        return render(request, "modify_room.html", ctx)

    def post(self, request, id):
        room = Room.objects.get(id=id)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector_available = request.POST.get('projector_available') == "on"
        if not name:
            ctx = {
                "room": room,
                "error": "No name typed in!"
            }
            return render(request, "modify_room.html", ctx)
        if capacity <= 0:
            ctx = {
                "room": room,
                "error": "Capacity cannot be lower than 0!"
            }
            return render(request, "modify_room.html", ctx)
        if name != room.name and Room.objects.filter(name=name).first():
            ctx = {
                "room": room,
                "error": "There is already a room with this name!"
            }
            return render(request, "modify_room.html", ctx)
        else:
            room.name = name
            room.capacity = capacity
            room.projector_available = projector_available
            room.save()
            return redirect("room-list")

class MakeReservation(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        ctx = {
            "room": room
        }
        return render(request, "make_reservation.html", ctx)

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        if date < str(datetime.date.today()):
            ctx = {
                "room": room,
                "error": "This date is in the past!"
            }
            return render(request, 'make_reservation.html', ctx)
        elif RoomReservation.objects.filter(room_id=room_id, date=date):
            ctx = {
                'room': room,
                'error': 'Room already taken!'
            }
            return render(request, 'make_reservation.html', ctx)
        else:
            RoomReservation.objects.create(room_id=room, date=date, comment=comment)
            return redirect("room-list")


