from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0004_alter_booking_total_price'),
    ]
    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_dismissed',
            field=models.BooleanField(default=False, help_text='If True, hidden from user dashboard'),
        ),
    ]
