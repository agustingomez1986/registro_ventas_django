# Generated by Django 5.2.1 on 2025-06-21 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_alter_venta_cuenta_transferencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventaitem',
            name='codigo_hacedor',
            field=models.CharField(choices=[('Ilanto', 'IL'), ('Aguaclara', 'AC'), ('Desopeton', 'DS')]),
        ),
    ]
