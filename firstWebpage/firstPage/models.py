from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Products(models.Model):
    product_name = models.CharField(max_length=30)
    quantity = models.FloatField()


class RawMaterial(models.Model):
    item_name = models.CharField(max_length=30)
    quantity = models.FloatField()
    unit = models.CharField(max_length=30)


class RawMaterialMapping(models.Model):
    raw_material_type = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    product_type = models.ForeignKey(Products, on_delete=models.CASCADE)
    no_of_parts_used = models.FloatField()


class ProductLog(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField(default=datetime.now().today().strftime('%Y-%m-%d'))
    time = models.TimeField(default=datetime.now().today().strftime('%H:%M:%S'))
    user_id = models.IntegerField()


class RawMaterialLog(models.Model):
    raw_material_id = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField(default=datetime.now().today().strftime('%Y-%m-%d'))
    time = models.TimeField(default=datetime.now().today().strftime('%H:%M:%S'))
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.IntegerField()


class MasterLog(models.Model):
    item_id = models.IntegerField()  # product id or raw material id
    item_log_id = models.IntegerField()  # product log id or raw material id
    quantity = models.FloatField()
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20)    # product or raw material
    action = models.CharField(max_length=20)        # add or update
    date = models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.today)
    user_id = models.IntegerField()


class ProductHistory:
    # log_id = models.IntegerField()
    # product_id = models.IntegerField()
    # product_name = models.CharField(max_length=30)
    # quantity = models.FloatField()
    # date = models.DateField(default=datetime.now().today().strftime('%Y-%m-%d'))
    # time = models.TimeField(default=datetime.now().today().strftime('%H:%M:%S'))
    pass
#
#
