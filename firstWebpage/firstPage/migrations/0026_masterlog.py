# Generated by Django 2.0.7 on 2018-09-07 18:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstPage', '0025_auto_20180906_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('item_log_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('item_type', models.CharField(max_length=10)),
                ('action', models.CharField(max_length=20)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('time', models.TimeField(default=datetime.datetime.today)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
