# Generated by Django 4.2.2 on 2023-07-07 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0032_customuser_password_confirm_alter_customuser_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password_confirm',
        ),
    ]