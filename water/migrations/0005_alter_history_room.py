# Generated by Django 4.0 on 2021-12-28 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0004_remove_historydetail_models_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='water.room'),
        ),
    ]
