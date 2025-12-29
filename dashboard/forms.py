from django import forms
from rooms.models import Room
from hotel.models import Slider, ContactInquiry
from booking.models import Booking

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'max_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'amenities': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'booking_status']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_status': forms.Select(attrs={'class': 'form-control'}),
        }

class ReplyInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['admin_reply']
        widgets = {
            'admin_reply': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
