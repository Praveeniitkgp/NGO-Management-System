# Generated migration - Renamed AdminUser to Admin
# This preserves all existing data

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_registereddonor_desired_donation_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminUser',
            new_name='Admin',
        ),
        migrations.AlterModelOptions(
            name='admin',
            options={'ordering': ['-created_at'], 'verbose_name': 'Admin', 'verbose_name_plural': 'Admins'},
        ),
    ]
