# Generated by Django 3.2.6 on 2021-09-25 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
