# Generated by Django 4.0 on 2022-01-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0007_historydetail_comlimentary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historydetail',
            name='comlimentary',
            field=models.IntegerField(default=0),
        ),
    ]
