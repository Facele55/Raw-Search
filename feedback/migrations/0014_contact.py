# Generated by Django 3.2.8 on 2022-05-22 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0013_auto_20220519_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
                'ordering': ['-timestamp'],
            },
        ),
    ]
