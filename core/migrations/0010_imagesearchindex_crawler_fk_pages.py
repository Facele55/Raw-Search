# Generated by Django 3.2.6 on 2021-09-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210923_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesearchindex',
            name='crawler_fk_pages',
            field=models.IntegerField(null=True),
        ),
    ]