# Generated by Django 3.2 on 2023-08-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=50),
        ),
    ]