from django.db import migrations
class Migration(migrations.Migration):
    dependencies = [
        ('rooms', '0003_alter_room_created_at_alter_room_room_number'),
    ]
    operations = [
        migrations.DeleteModel(
            name='RoomImage',
        ),
    ]
