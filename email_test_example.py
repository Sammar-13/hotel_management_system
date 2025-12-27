import os
import django
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_miramar_sg.settings')
django.setup()

def test_send_email():
    """
    Test sending an email using the configured SMTP backend.
    """
    print("\n--- Django Email Test ---")
    recipient = input("Enter recipient email address: ").strip()
    if not recipient:
        print("No recipient provided. Exiting.")
        return

    subject = 'Test Email from Hotel Miramar SG'
    message = 'This is a test email to verify Gmail SMTP configuration.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient] 

    print(f"\nConfiguration:")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"FROM: {from_email}")
    
    try:
        print(f"\nAttempting to send email to {recipient}...")
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print("SUCCESS: Email sent successfully!")
        print("Check your inbox (and spam folder).")
    except Exception as e:
        print(f"FAILURE: Failed to send email.")
        print(f"Error: {e}")
        print("\n--- Troubleshooting Tips ---")
        print("1. Check internet connection.")
        print("2. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env file.")
        print("3. If using Gmail, ensure you are using an App Password, not your login password.")

if __name__ == '__main__':
    test_send_email()
