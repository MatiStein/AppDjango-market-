# Generated by Django 4.1.4 on 2023-01-04 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_users_profileuser_usermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='tickers',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
