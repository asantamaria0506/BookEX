# Generated by Django 4.2.7 on 2023-11-25 17:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookMng', '0007_book_ownedby'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='ownedby',
        ),
        migrations.AddField(
            model_name='book',
            name='ownedby',
            field=models.ManyToManyField(blank=True, related_name='owned_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
