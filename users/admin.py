from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.contrib.admin import helpers
from .models import User, UserProfile
from .forms import AdminEmailForm

def send_email_action(modeladmin, request, queryset):
    """
    Admin action to send email to selected users.
    """
    if 'post' in request.POST:
        form = AdminEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            count = 0
            
            # Send to users with email addresses
            users_with_email = queryset.exclude(email='')
            
            # Log usage (print to console/server log as requested)
            print(f"Admin {request.user.username} initiating email blast to {users_with_email.count()} users.")
            print(f"Subject: {subject}")

            for user in users_with_email:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    count += 1
                except Exception as e:
                    # Log error
                    print(f"Failed to send to {user.email}: {e}")
                    modeladmin.message_user(request, f"Error sending to {user.email}: {e}", level=messages.ERROR)
            
            modeladmin.message_user(request, f"Successfully sent email to {count} user(s).", level=messages.SUCCESS)
            return None # Return None to return to the change list
            
    else:
        form = AdminEmailForm()

    users_without_email = queryset.filter(email='')
    
    context = {
        'title': 'Send Email to Users',
        'form': form,
        'queryset': queryset,
        'opts': modeladmin.model._meta,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'users_without_email': users_without_email,
        'media': modeladmin.media,
    }
    
    return render(request, 'admin/users/user/send_email.html', context)

send_email_action.short_description = "Send email to selected users"
send_email_action.allowed_permissions = ('change',)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active', 'role')
    list_filter = ()  # Remove side filters
    filter_horizontal = ()  # Remove groups/permissions widget
    actions = ['delete_selected', send_email_action]

    # Custom fieldsets to remove Groups and User Permissions
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'role')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'role',)}),
    )

    def has_delete_permission(self, request, obj=None):
        # Superusers can delete anyone.
        if request.user.is_superuser:
            return True
        
        # Prevent non-superusers from deleting anyone (including themselves).
        # More granular permission can be added here if needed.
        return False

admin.site.register(User, UserAdmin)