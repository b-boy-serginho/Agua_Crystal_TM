# Generated by Django 5.2.3 on 2025-07-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_factura_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='importe_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
