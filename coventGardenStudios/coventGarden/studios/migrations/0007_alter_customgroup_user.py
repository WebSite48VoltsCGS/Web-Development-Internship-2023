# Generated by Django 4.2.2 on 2023-06-28 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0006_remove_customgroup_id_alter_customgroup_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]