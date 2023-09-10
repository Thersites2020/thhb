# Generated by Django 4.2.5 on 2023-09-09 15:34

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('subtitle', models.CharField(max_length=250)),
                ('author', models.CharField(default='Nicholas Thorne', max_length=50)),
                ('image', models.ImageField(upload_to='static/img/')),
                ('image_alt', models.CharField(max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('MN', 'Main'), ('RL', 'Related'), ('OT', 'Other')], default='MN', max_length=2)),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]