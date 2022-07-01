# Generated by Django 3.2.8 on 2022-05-19 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_autocomplete_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autocomplete',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='autocomplete',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20, verbose_name='Status'),
        ),
    ]