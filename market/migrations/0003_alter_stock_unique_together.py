# Generated by Django 4.1.3 on 2022-12-10 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_irregularstocksdates_alter_stock_ticker_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('ticker', 'time')},
        ),
    ]
