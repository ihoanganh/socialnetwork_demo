# Generated by Django 5.0.1 on 2024-02-22 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]