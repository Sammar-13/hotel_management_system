from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .decorators import admin_required
from .forms import RoomForm, SliderForm, AdminBookingForm, ReplyInquiryForm

from rooms.models import Room
from booking.models import Booking
from hotel.models import ContactInquiry, Feedback, Slider

User = get_user_model()

@admin_required
def dashboard_home(request):
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(booking_status='pending').count()
    total_users = User.objects.count()
    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    
    context = {
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_users': total_users,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard/home.html', context)

# --- Room Management ---

@admin_required
def manage_rooms(request):
    rooms_list = Room.objects.all().order_by('room_number')
    paginator = Paginator(rooms_list, 10)
    page_number = request.GET.get('page')
    rooms = paginator.get_page(page_number)
    return render(request, 'dashboard/rooms/manage_rooms.html', {'rooms': rooms})

@admin_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully!')
            return redirect('dashboard:manage_rooms')
    else:
        form = RoomForm()
    return render(request, 'dashboard/rooms/add_room.html', {'form': form, 'title': 'Add New Room'})

@admin_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('dashboard:manage_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'dashboard/rooms/add_room.html', {'form': form, 'title': f'Edit Room: {room.room_name}'})

@admin_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('dashboard:manage_rooms')
    return render(request, 'dashboard/confirm_delete.html', {'object': room, 'type': 'Room'})

# --- Booking Management ---

@admin_required
def manage_bookings(request):
    bookings_list = Booking.objects.all().order_by('-created_at')
    
    # Simple Filter
    status = request.GET.get('status')
    if status:
        bookings_list = bookings_list.filter(booking_status=status)

    paginator = Paginator(bookings_list, 10)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)
    return render(request, 'dashboard/bookings/manage_bookings.html', {'bookings': bookings})

@admin_required
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = AdminBookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking_obj = form.save(commit=False)
            
            # Recalculate price if dates changed
            if 'check_in_date' in form.changed_data or 'check_out_date' in form.changed_data:
                num_nights = (booking_obj.check_out_date - booking_obj.check_in_date).days
                if num_nights > 0:
                    booking_obj.total_price = num_nights * booking_obj.room.price_per_night
            
            if booking_obj.booking_status == 'cancelled' and not booking_obj.is_cancelled:
                booking_obj.is_cancelled = True
                booking_obj.cancelled_at = timezone.now()
            booking_obj.save()
            messages.success(request, f'Booking details updated.')
            return redirect('dashboard:manage_bookings')
    else:
        form = AdminBookingForm(instance=booking)
    return render(request, 'dashboard/bookings/update_booking.html', {'form': form, 'booking': booking})

# --- User Management ---

@admin_required
def manage_users(request):
    users_list = User.objects.exclude(is_superuser=True).order_by('-date_joined')
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    return render(request, 'dashboard/users/manage_users.html', {'users': users})

@admin_required
def delete_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.is_superuser:
        messages.error(request, "Cannot delete a superuser.")
        return redirect('dashboard:manage_users')
        
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('dashboard:manage_users')
    return render(request, 'dashboard/confirm_delete.html', {'object': user_obj, 'type': 'User'})

@admin_required
def toggle_user_active(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.is_superuser:
        messages.error(request, "Cannot block a superuser.")
        return redirect('dashboard:manage_users')
    
    if request.method == 'POST':
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status = 'unblocked' if user_obj.is_active else 'blocked'
        messages.success(request, f'User {user_obj.username} has been {status}.')
        return redirect('dashboard:manage_users')
    
    # Optional: Confirmation page logic if needed, but for toggle usually direct POST or button form is used.
    # Assuming direct POST from manage_users page for simplicity, or we can make it a simple redirect if used via GET (not recommended for state change but acceptable for simple toggle if safe)
    # Better to keep it safe. If GET, show confirmation? No, let's assume POST from form.
    # But for a simple toggle button, often people use GET link. To be strict, use POST.
    return redirect('dashboard:manage_users')

# --- Feedback Management ---

@admin_required
def manage_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedback_list, 10)
    page_number = request.GET.get('page')
    feedbacks = paginator.get_page(page_number)
    return render(request, 'dashboard/feedback/manage_feedback.html', {'feedbacks': feedbacks})

@admin_required
def delete_feedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully!')
        return redirect('dashboard:manage_feedback')
    return render(request, 'dashboard/confirm_delete.html', {'object': feedback, 'type': 'Feedback'})

# --- Slider Management ---

@admin_required
def manage_sliders(request):
    sliders = Slider.objects.all()
    return render(request, 'dashboard/sliders/manage_sliders.html', {'sliders': sliders})

@admin_required
def add_slider(request):
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider added successfully!')
            return redirect('dashboard:manage_sliders')
    else:
        form = SliderForm()
    return render(request, 'dashboard/sliders/add_slider.html', {'form': form, 'title': 'Add New Slider'})

@admin_required
def edit_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider updated successfully!')
            return redirect('dashboard:manage_sliders')
    else:
        form = SliderForm(instance=slider)
    return render(request, 'dashboard/sliders/add_slider.html', {'form': form, 'title': 'Edit Slider'})

@admin_required
def delete_slider(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, 'Slider deleted successfully!')
        return redirect('dashboard:manage_sliders')
    return render(request, 'dashboard/confirm_delete.html', {'object': slider, 'type': 'Slider'})

@admin_required
def toggle_slider_active(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        slider.is_active = not slider.is_active
        slider.save()
        status = 'activated' if slider.is_active else 'deactivated'
        messages.success(request, f'Slider "{slider.title}" has been {status}.')
    return redirect('dashboard:manage_sliders')

# --- Inquiry Management ---

@admin_required
def manage_inquiries(request):
    inquiries_list = ContactInquiry.objects.all().order_by('-created_at')
    paginator = Paginator(inquiries_list, 10)
    page_number = request.GET.get('page')
    inquiries = paginator.get_page(page_number)
    return render(request, 'dashboard/inquiries/manage_inquiries.html', {'inquiries': inquiries})

@admin_required
def reply_inquiry(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    if request.method == 'POST':
        form = ReplyInquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.is_replied = True
            reply.replied_at = timezone.now()
            reply.save()
            # Here you would typically send an email
            messages.success(request, 'Reply saved successfully!')
            return redirect('dashboard:manage_inquiries')
    else:
        form = ReplyInquiryForm(instance=inquiry)
    return render(request, 'dashboard/inquiries/reply_inquiry.html', {'form': form, 'inquiry': inquiry})