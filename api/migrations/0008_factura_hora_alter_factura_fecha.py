# Generated by Django 5.2.3 on 2025-07-05 21:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_producto_imagen_alter_ubicacion_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
