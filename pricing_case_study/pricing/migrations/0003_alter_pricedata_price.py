# Generated by Django 5.1.4 on 2024-12-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_alter_pricedata_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricedata',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
