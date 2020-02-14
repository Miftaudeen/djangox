# Generated by Django 3.0.3 on 2020-02-14 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            ],
        ),
    ]