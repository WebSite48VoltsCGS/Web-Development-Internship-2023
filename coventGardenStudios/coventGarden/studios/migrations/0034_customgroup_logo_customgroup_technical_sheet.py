# Generated by Django 4.2.2 on 2023-07-07 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0033_remove_customuser_password_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroup',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='media/public', verbose_name='Logo'),
        ),
        migrations.AddField(
            model_name='customgroup',
            name='technical_sheet',
            field=models.FileField(blank=True, null=True, upload_to='media/public', verbose_name='Fiche technique'),
        ),
    ]