# Generated by Django 2.2.28 on 2023-09-17 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_playercharacter_dead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Discord Nickname'),
        ),
    ]