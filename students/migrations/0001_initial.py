# Generated by Django 3.0.7 on 2020-06-15 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('venue', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.TextField()),
                ('hostel', models.ManyToManyField(related_name='rooms', to='students.Hostel')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matric_num', models.CharField(max_length=15)),
                ('surname', models.TextField()),
                ('firstname', models.TextField()),
                ('othername', models.TextField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'), ('Unknown', 'Unknown')], default='Male', max_length=10)),
                ('programme', models.TextField()),
                ('payment_status', models.CharField(choices=[('no', 'No Payment'), ('partial', 'Partial Payment'), ('full', 'Full Payment')], default='no', max_length=20)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='students.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('phone_number', models.TextField()),
                ('address', models.TextField(blank=True, null=True)),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='VisitingStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_visitors', to='students.Student')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_time', models.DateTimeField()),
                ('other_supervisor', models.TextField()),
                ('remark', models.CharField(max_length=5000)),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examination_supervisors', to='students.Examination')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_attendances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('day', models.DateField()),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('moving', models.CharField(choices=[('in', 'In'), ('out', 'Out')], max_length=3)),
                ('mover', models.TextField()),
                ('timestamp', models.DateTimeField(null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_properties', to='students.Student')),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='PorterAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField(blank=True, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hostel_porter_attendance', to='students.Hostel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='porter_attendances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HostelAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False)),
                ('remark', models.TextField(blank=True, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Hostel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.TimeField()),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Examination')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
            options={
                'unique_together': {('student', 'exam')},
            },
        ),
    ]
