# Generated by Django 3.0.3 on 2020-02-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='payment_status',
            field=models.CharField(choices=[('no', 'No Payment'), ('partial', 'Partial Payment'), ('full', 'Full Payment')], default='no', max_length=20),
        ),
    ]