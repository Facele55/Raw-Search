# Generated by Django 3.2.6 on 2021-09-07 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210907_1232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentsearchindex',
            options={'verbose_name': 'Content Search Index', 'verbose_name_plural': 'Content Search Indexes'},
        ),
        migrations.AlterModelOptions(
            name='imagesearchindex',
            options={'verbose_name': 'Image Search Index', 'verbose_name_plural': 'Image Search Indexes'},
        ),
        migrations.AlterModelOptions(
            name='searchqueries',
            options={'verbose_name': 'Search Query', 'verbose_name_plural': 'Search Queries'},
        ),
    ]
