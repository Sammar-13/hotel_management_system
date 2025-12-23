import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_miramar_sg.settings')
django.setup()

def test_send_email():
    """
    Test sending an email using the configured SMTP backend.
    """
    subject = 'Test Email from Hotel Miramar SG'
    message = 'This is a test email to verify Gmail SMTP configuration.'
    from_email = settings.DEFAULT_FROM_EMAIL
    # Replace with a recipient email you can check
    recipient_list = ['test_recipient@example.com'] 

    try:
        print(f"Attempting to send email from: {from_email}...")
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        print("\n--- Troubleshooting Tips ---")
        print("1. Ensure 'Less secure app access' is ON or you are using an App Password.")
        print("2. Check your internet connection.")
        print("3. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py.")

def switch_to_console_backend():
    """
    Instructions for switching to Console Backend for local testing.
    """
    print("\n--- Local Testing Fallback ---")
    print("If SMTP fails or for development, switch to Console Backend:")
    print("In 'hotel_miramar_sg/settings.py', set:")
    print("EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'")
    print("This will print emails to the terminal instead of sending them.")

if __name__ == '__main__':
    test_send_email()
    switch_to_console_backend()
