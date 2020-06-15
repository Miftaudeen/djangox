# Generated by Django 3.0.3 on 2020-06-11 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0019_hostelattendance_remark'),
    ]

    operations = [
        migrations.CreateModel(
            name='PorterAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hostel_porter_attendance', to='students.Hostel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='porter_attendances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
    ]