# Generated by Django 4.0 on 2021-12-28 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0005_alter_history_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='historydetail',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
