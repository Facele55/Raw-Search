# Generated by Django 3.2.6 on 2021-09-06 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20210906_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='results_was_helpful',
            field=models.CharField(choices=[('no', 'NO'), ('yes', 'YES')], default='', max_length=3, null=True),
        ),
    ]
