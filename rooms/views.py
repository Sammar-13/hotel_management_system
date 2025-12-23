from django.shortcuts import render, get_object_or_404
from .models import Room, Amenity
from django.db.models import Q

def room_list(request):
    query = request.GET.get('q')
    room_type = request.GET.get('room_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(Q(room_name__icontains=query) | Q(description__icontains=query))
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)

    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)

    room_types = Room.ROOM_TYPE_CHOICES
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
        'selected_room_type': room_type,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
    }
    return render(request, 'rooms/room_list.html', context)

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {
        'room': room,
    }
    return render(request, 'rooms/room_detail.html', context)