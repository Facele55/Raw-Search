# Generated by Django 3.2.6 on 2021-09-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlersites',
            name='optional_field_1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='crawlersites',
            name='optional_field_2',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='crawlersites',
            name='optional_field_3',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='crawlersites',
            name='optional_field_4',
            field=models.TextField(null=True),
        ),
    ]