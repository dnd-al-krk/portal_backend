# Generated by Django 2.2.9 on 2020-02-01 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("games", "0013_auto_20190825_1356")]

    operations = [
        migrations.AddField(
            model_name="table", name="extra_notes", field=models.TextField(blank=True, verbose_name="Table extra notes")
        )
    ]