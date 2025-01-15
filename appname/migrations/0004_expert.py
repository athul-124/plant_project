# Generated by Django 5.1.4 on 2025-01-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appname', '0003_plant_spaceimage_delete_plants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('expertise', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='experts/')),
            ],
        ),
    ]
