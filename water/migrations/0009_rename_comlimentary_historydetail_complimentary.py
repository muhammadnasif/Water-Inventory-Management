# Generated by Django 4.0 on 2022-01-05 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0008_alter_historydetail_comlimentary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historydetail',
            old_name='comlimentary',
            new_name='complimentary',
        ),
    ]
