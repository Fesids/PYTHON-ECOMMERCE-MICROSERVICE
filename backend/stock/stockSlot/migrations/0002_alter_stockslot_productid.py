# Generated by Django 4.1.10 on 2023-10-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockSlot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockslot',
            name='productId',
            field=models.IntegerField(unique=True),
        ),
    ]
