# Generated by Django 2.0.7 on 2018-08-14 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstPage', '0017_auto_20180809_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlog',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstPage.Products'),
        ),
        migrations.AlterField(
            model_name='rawmateriallog',
            name='raw_material_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstPage.RawMaterial'),
        ),
    ]
