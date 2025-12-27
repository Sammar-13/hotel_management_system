import django.utils.timezone
from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_remove_user_address_remove_user_phone_number_and_more'),
    ]
    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
