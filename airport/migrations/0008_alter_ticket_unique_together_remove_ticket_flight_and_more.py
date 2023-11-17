# Generated by Django 4.2.6 on 2023-11-17 19:32

import airport.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0007_crew_image"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="flight",
        ),
        migrations.RemoveField(
            model_name="ticket",
            name="order",
        ),
        migrations.AlterField(
            model_name="crew",
            name="image",
            field=models.ImageField(
                null=True, upload_to=airport.utils.crew_image_file_path
            ),
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.DeleteModel(
            name="Ticket",
        ),
    ]
