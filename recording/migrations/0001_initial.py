# Generated by Django 3.2.9 on 2021-12-12 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_Main_Img', models.ImageField(upload_to='static/media/')),
            ],
        ),
    ]