# Generated by Django 2.0.7 on 2020-05-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstPage', '0048_auto_20190817_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlog',
            name='date',
            field=models.DateField(default='2020-05-25'),
        ),
        migrations.AlterField(
            model_name='productlog',
            name='time',
            field=models.TimeField(default='23:41:03'),
        ),
        migrations.AlterField(
            model_name='rawmateriallog',
            name='date',
            field=models.DateField(default='2020-05-25'),
        ),
        migrations.AlterField(
            model_name='rawmateriallog',
            name='time',
            field=models.TimeField(default='23:41:03'),
        ),
    ]
