# Generated by Django 3.0.3 on 2020-03-01 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_studentlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentlog',
            name='matric_num',
        ),
        migrations.AddField(
            model_name='studentlog',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student'),
        ),
    ]