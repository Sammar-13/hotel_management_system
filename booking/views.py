from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from rooms.models import Room
from .forms import BookingForm
from django.db.models import Q
from datetime import date

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']

            # Basic availability check (more complex logic will be needed)
            if check_in >= check_out:
                messages.error(request, 'Check-out date must be after check-in date.')
                return render(request, 'booking/book_room.html', {'room': room, 'form': form})
            
            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                room=room,
                booking_status__in=['pending', 'approved'],
                check_in_date__lt=check_out,
                check_out_date__gt=check_in
            ).count()

            if overlapping_bookings > 0:
                messages.error(request, 'This room is not available for the selected dates.')
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.room = room
                # Calculate total price (simple calculation for now)
                num_nights = (check_out - check_in).days
                booking.total_price = num_nights * room.price_per_night
                booking.save()
                messages.success(request, 'Room booked successfully! Your booking is pending approval.')
                return redirect('my_bookings')
        else:
            messages.error(request, 'Error with your booking. Please check the dates.')
    else:
        form = BookingForm()
    return render(request, 'booking/book_room.html', {'room': room, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.booking_status == 'pending':
        booking.booking_status = 'cancelled'
        booking.save()
        messages.info(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'Bookings that are not pending cannot be cancelled via this page.')
    return redirect('my_bookings')