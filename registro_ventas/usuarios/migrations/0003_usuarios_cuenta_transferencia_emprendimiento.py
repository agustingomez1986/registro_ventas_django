# Generated by Django 5.2.1 on 2025-06-27 20:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuarios_interno'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='cuenta_transferencia',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Emprendimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_emprendimiento', models.CharField(max_length=50, unique=True)),
                ('codigo_emprendimiento', models.CharField(max_length=4, unique=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprendimiento', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
