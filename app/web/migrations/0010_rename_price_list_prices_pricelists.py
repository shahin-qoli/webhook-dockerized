# Generated by Django 4.0.4 on 2022-05-30 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_remove_pricelists_option_value_pricelists_brand'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prices',
            old_name='price_list',
            new_name='PriceLists',
        ),
    ]
