# Generated by Django 3.0.8 on 2020-09-10 13:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20200910_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
