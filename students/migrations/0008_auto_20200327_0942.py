# Generated by Django 3.0.3 on 2020-03-27 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20200326_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='hostel',
            field=models.ManyToManyField(related_name='rooms', to='students.Hostel'),
        ),
        migrations.AlterField(
            model_name='student',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='students.Room'),
        ),
        migrations.AlterUniqueTogether(
            name='hostelattendance',
            unique_together=set(),
        ),
    ]
