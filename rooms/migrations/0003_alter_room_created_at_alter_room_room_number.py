import django.utils.timezone
from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0002_remove_room_category_alter_amenity_options_and_more'),
    ]
    operations = [
        migrations.AlterField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
