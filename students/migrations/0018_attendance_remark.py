# Generated by Django 3.0.3 on 2020-06-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_auto_20200608_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='remark',
            field=models.TextField(blank=True, null=True),
        ),
    ]
