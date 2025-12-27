from django.db import models
from django.conf import settings
class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True, null=True, help_text="The reply from the admin.")
    is_replied = models.BooleanField(default=False)
    replied_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        verbose_name_plural = "Contact Inquiries"
    def __str__(self):
        return f"Inquiry from {self.name} - {self.subject or 'No Subject'}"
class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='slider/')
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Sliders"
    def __str__(self):
        return self.title
class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) 
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Feedback"
    def __str__(self):
        return f"Feedback by {self.user.username} - Rating: {self.rating}"
