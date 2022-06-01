# Generated by Django 4.0.4 on 2022-05-26 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=0, max_digits=200)),
                ('price_date', models.CharField(max_length=200)),
                ('import_title', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('data', models.JSONField()),
                ('event_created_at', models.DateTimeField()),
                ('event_id', models.IntegerField(primary_key=True, serialize=False)),
                ('event_type', models.CharField(max_length=200)),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SpreeOptionValues',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('position', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('presentation', models.CharField(max_length=200)),
                ('option_type_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SpreeProducts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('available_on', models.DateField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('tax_category_id', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('discontinue_on', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SpreeVariants',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('sku', models.CharField(max_length=200)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_master', models.BooleanField()),
                ('cost_price', models.DecimalField(blank=True, decimal_places=0, max_digits=200, null=True)),
                ('track_inventory', models.BooleanField()),
                ('tax_category_id', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('discontinue_on', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreeproducts')),
            ],
        ),
        migrations.CreateModel(
            name='SpreePrices',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=200)),
                ('currency', models.CharField(max_length=200)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('compare_at_amount', models.DecimalField(blank=True, decimal_places=0, max_digits=200, null=True)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreevariants')),
            ],
        ),
        migrations.CreateModel(
            name='SpreeOptionValueVariants',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('option_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreeoptionvalues')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreevariants')),
            ],
        ),
        migrations.CreateModel(
            name='PriceLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField()),
                ('start_at', models.DateField(blank=True, null=True)),
                ('end_at', models.DateField(blank=True, null=True)),
                ('retailer_discount', models.DecimalField(blank=True, decimal_places=3, max_digits=200, null=True)),
                ('distributer_discount', models.DecimalField(blank=True, decimal_places=3, max_digits=200, null=True)),
                ('retailer_cheque_discount', models.DecimalField(blank=True, decimal_places=3, max_digits=200, null=True)),
                ('distributer_cheque_discount', models.DecimalField(blank=True, decimal_places=3, max_digits=200, null=True)),
                ('cheque_time', models.IntegerField(blank=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.brands')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=200)),
                ('created_date', models.DateTimeField()),
                ('price_date', models.DateTimeField(null=True)),
                ('price_source', models.CharField(default=None, max_length=200)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreevariants')),
            ],
        ),
        migrations.AddField(
            model_name='brands',
            name='option_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.spreeoptionvalues'),
        ),
    ]
