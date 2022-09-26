# Generated by Django 3.2.12 on 2022-09-25 08:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rule', models.CharField(choices=[('based_on_order', 'Based On Order Amount'), ('based_on_quantity', 'Based On Quantity')], max_length=40)),
                ('discount_type', models.CharField(choices=[('fixed_price', 'Fixed Price'), ('percentage', 'Percentage')], max_length=40)),
                ('discount_value', models.FloatField()),
                ('message', models.CharField(max_length=200)),
                ('is_enable', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cost_price', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('description', models.CharField(max_length=200)),
                ('barcode', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
                ('discount_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakery.discount')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('amount', models.FloatField()),
                ('order_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakery.product')),
            ],
        ),
    ]
