from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone
from .models import ContactInquiry, Feedback, Slider

class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_replied')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ()
    ordering = ('-created_at',)
    
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at', 'replied_at')
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Admin Response', {
            'fields': ('admin_reply', 'is_replied', 'replied_at')
        }),
    )

    def save_model(self, request, obj, form, change):
       
        if obj.admin_reply and 'admin_reply' in form.changed_data:
            obj.is_replied = True
            obj.replied_at = timezone.now()


            subject = f"Reply to your inquiry: '{obj.subject}'"
            body = (
                f"Hi {obj.name},\n\n"
                f"Thank you for your inquiry. Here is our response:\n\n"
                f"------------------------------------\n"
                f"Your Original Message:\n"
                f"'{obj.message}'\n"
                f"------------------------------------\n\n"
                f"Our Reply:\n"
                f"{obj.admin_reply}\n\n"
                f"Best regards,\n"
                f"The Hotel Miramar SG Team"
            )
            
            try:
                # Force the 'from' email to ensure all replies are sent from a consistent address
                from_email = 'sammarabbas9939@gmail.com'
                send_mail(
                    subject,
                    body,
                    from_email,
                    [obj.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Add a message to the admin interface if the email fails
                self.message_user(request, f"The reply was saved, but the email could not be sent. Error: {e}", level='error')

        super().save_model(request, obj, form, change)


# Admin configuration for Feedback model
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ()
    ordering = ('-created_at',)
    readonly_fields = ('user', 'created_at', 'rating', 'message',)

# Admin configuration for Slider model
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    search_fields = ('title', 'subtitle')

# Register your models here with their custom Admin classes
admin.site.register(ContactInquiry, ContactInquiryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Slider, SliderAdmin)