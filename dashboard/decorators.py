from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access the dashboard.")
            return redirect('login')
        
        if request.user.role == 'admin' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')
    return _wrapped_view

def user_required(view_func):
    """
    Decorator to ensure that the user is NOT an admin.
    If the user is an admin, they are redirected to the admin dashboard.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser):
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
