# Generated by Django 5.2.3 on 2025-07-02 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_factura_importe_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='clientes/'),
        ),
    ]
