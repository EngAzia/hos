# Generated by Django 3.0.5 on 2021-10-02 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_auto_20210921_0131'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='appointment',
            table='appointment',
        ),
        migrations.DeleteModel(
            name='patientstatu',
        ),
    ]
