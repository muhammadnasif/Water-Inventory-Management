# Generated by Django 4.0 on 2022-01-05 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0009_rename_comlimentary_historydetail_complimentary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historydetail',
            name='complimentary',
            field=models.IntegerField(default=1),
        ),
    ]
