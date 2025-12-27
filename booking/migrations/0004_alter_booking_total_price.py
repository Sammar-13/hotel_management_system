from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0003_alter_booking_options_remove_booking_status_and_more'),
    ]
    operations = [
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
