# Generated by Django 4.2.7 on 2024-02-20 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0006_company_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="is_top",
            field=models.BooleanField(default=False),
        ),
    ]