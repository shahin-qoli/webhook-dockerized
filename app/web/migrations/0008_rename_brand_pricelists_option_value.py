# Generated by Django 4.0.4 on 2022-05-30 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_alter_pricelists_brand_alter_pricelists_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricelists',
            old_name='brand',
            new_name='option_value',
        ),
    ]