# Generated by Django 3.0.3 on 2020-06-11 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200611_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='staff_id_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
