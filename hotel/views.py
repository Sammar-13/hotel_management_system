from django.shortcuts import render, redirect
from .models import Slider, ContactInquiry, Feedback
from .forms import ContactForm, FeedbackForm
from rooms.models import Room
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    sliders = Slider.objects.filter(is_active=True)
    rooms = Room.objects.all()[:3] # Show a few rooms on homepage
    context = {
        'sliders': sliders,
        'rooms': rooms,
    }
    return render(request, 'hotel/home.html', context)

def about(request):
    return render(request, 'hotel/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'hotel/contact.html', {'form': form})

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.user = request.user
            feedback_instance.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'hotel/feedback.html', {'form': form})