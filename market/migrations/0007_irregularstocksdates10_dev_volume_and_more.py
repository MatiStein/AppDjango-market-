# Generated by Django 4.1.3 on 2022-12-17 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_irregularstocksdates5'),
    ]

    operations = [
        migrations.AddField(
            model_name='irregularstocksdates10',
            name='dev_volume',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='irregularstocksdates10',
            name='avg_volume',
            field=models.DecimalField(decimal_places=4, max_digits=24),
        ),
        migrations.AlterField(
            model_name='irregularstocksdates10',
            name='volume',
            field=models.DecimalField(decimal_places=4, max_digits=24),
        ),
    ]
