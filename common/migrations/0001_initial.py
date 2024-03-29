# Generated by Django 4.2.7 on 2024-02-20 11:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=256)),
                ("image", models.ImageField(upload_to="news/")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
