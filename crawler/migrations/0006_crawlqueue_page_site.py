# Generated by Django 3.2.8 on 2022-06-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_crawlqueue_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlqueue',
            name='page_site',
            field=models.CharField(choices=[('page', 'Page'), ('site', 'Site')], default='empty', max_length=20),
        ),
    ]