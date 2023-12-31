# Generated by Django 4.1.10 on 2023-11-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('products', models.ManyToManyField(null=True, related_name='products', to='product.product')),
            ],
        ),
    ]
