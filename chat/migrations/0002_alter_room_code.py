# Generated by Django 4.2.4 on 2023-10-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="code",
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
