# Generated by Django 4.2.2 on 2023-07-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0027_customuser_phone_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalsheet',
            name='pdf_logo',
            field=models.FileField(null=True, upload_to='logo/public'),
        ),
    ]
