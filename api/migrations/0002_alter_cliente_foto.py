# Generated by Django 5.2.3 on 2025-07-02 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='foto',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
