# Generated by Django 4.0.4 on 2022-05-30 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_spreeproducts_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='distributer_price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prices',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prices',
            name='retailer_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
