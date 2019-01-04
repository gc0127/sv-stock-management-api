from copy import deepcopy
from datetime import datetime

import jsonpickle as jsonpickle
from django.core import serializers
from .serializers import RawMaterialSerializer, ProductSerializer, ProductLogSerializer, RawMaterialLogSerializer, \
    RawMaterialMappingSerializer, MasterLogSerializer, ProductLogNameSerializer, ProductHistorySerializer
from .models import RawMaterial, Products, ProductLog, RawMaterialLog, RawMaterialMapping, ProductHistory
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
from django.http import HttpResponse

'''get and post request methods for stock'''


@api_view(['GET', 'POST'])
def stocks_list(request):
    
    if request.method == 'GET':
        queryset = RawMaterial.objects.all()
        queryset = queryset.exclude(item_name='Armature')
        serializer = RawMaterialSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        stock = RawMaterial.objects.get(id=request.data['id'])
        stock_qty = stock.quantity

        '''For storing data in  Raw Material Log'''
        log_ser = RawMaterialLogSerializer(data=request.data)
        log_ser.initial_data['raw_material_id'] = request.data['id']
        log_ser.initial_data['date'] = datetime.now().today().strftime('%Y-%m-%d')
        log_ser.initial_data['time'] = datetime.now().today().strftime('%H:%M:%S')
        if log_ser.is_valid():
            new_log = log_ser.save()

        '''For Storing data in Master Log'''
        master_log_ser = MasterLogSerializer(data=request.data)
        master_log_ser.initial_data['item_id'] = request.data['id']
        master_log_ser.initial_data['item_log_id'] = new_log.id
        master_log_ser.initial_data['item_type'] = "rawMaterial"
        master_log_ser.initial_data['action'] = "ADD"
        master_log_ser.initial_data['date'] = new_log.date
        master_log_ser.initial_data['time'] = new_log.time
        if master_log_ser.is_valid():
            master_log_ser.save()

        new_data = request.data
        new_data['item_name'] = stock.item_name
        new_data['unit'] = stock.unit
        new_data['quantity'] = new_data['quantity'] + stock_qty

        serializer = RawMaterialSerializer(stock, data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def stock_detail(request, pk):
    try:
        stock = RawMaterial.objects.get(pk=pk)
    except RawMaterial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RawMaterialSerializer(stock)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_list(request):

        if request.method == "GET":
            queryset = Products.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)

        if request.method == 'POST':

            product = Products.objects.get(id=request.data['id'])
            qty = product.quantity

            '''For String data in Product Log'''
            log_ser = ProductLogSerializer(data=request.data)
            log_ser.initial_data['product_id'] = request.data['id']
            log_ser.initial_data['date'] = datetime.now().today().strftime('%Y-%m-%d')
            log_ser.initial_data['time'] = datetime.now().today().strftime('%H:%M:%S')
            if log_ser.is_valid():
                new_log = log_ser.save()

            '''For Storing data in Master Log'''
            master_log_ser = MasterLogSerializer(data=request.data)
            master_log_ser.initial_data['item_id'] = request.data['id']
            master_log_ser.initial_data['item_log_id'] = new_log.id
            master_log_ser.initial_data['item_type'] = "product"
            if request.data['quantity'] > 0:
                master_log_ser.initial_data['action'] = "ADD"
            else:
                master_log_ser.initial_data['action'] = "SALE"
            master_log_ser.initial_data['date'] = new_log.date
            master_log_ser.initial_data['time'] = new_log.time
            if master_log_ser.is_valid():
                master_log_ser.save()
            print(master_log_ser.errors)

            product_qty = request.data['quantity']
            p_id = request.data['id']
            if product_qty > 0:
                item_list = RawMaterialMapping.objects.filter(product_type_id=p_id)
                for item in item_list:
                    no_of_parts = item.no_of_parts_used
                    rm_id = item.raw_material_type_id
                    raw_material = RawMaterial.objects.get(id=rm_id)
                    raw_material.quantity = raw_material.quantity - product_qty * no_of_parts
                    if raw_material.item_name == 'Armature':
                        arm_prod = Products.objects.get(product_name="Armature")
                        arm_prod.quantity = raw_material.quantity
                        arm_prod.save()
                    raw_material.save()

            new_data = request.data
            prod = Products.objects.get(id=p_id)
            prod_name = prod.product_name
            new_data['quantity'] = new_data['quantity'] + qty
            new_data['product_name'] = prod_name

            if p_id == 6:  # request.data['id']
                armature_obj = RawMaterial.objects.get(item_name='Armature')
                armature_obj.quantity = new_data['quantity']
                armature_obj.save()

            serializer = ProductSerializer(product, data=new_data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_detail(request, pk):

    try:
        product = Products.objects.get(id=pk)
        qty = product.quantity
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_log_list(request):
    if request.method == 'GET':

        prod_log = ProductLog.objects.all()
        new_prod_log = []
        new_prod_log_dict = []
        # prods = ProductLog.objects.all().select_related('product_id')
        for p in prod_log:
            log = ProductHistory()
            log.log_id = str(p.id)
            # log.product_id = str(p.product_id)
            log.quantity = p.quantity
            log.date = str(p.date)
            log.time = str(p.time)
            log.product_name = str(p.product_id.product_name)
            new_prod_log.append(log)

        for log in new_prod_log:
            new_prod_log_dict.append(log.__dict__)

        jsondata = json.dumps(new_prod_log_dict)
        print(jsondata)
        # print(jsonpickle.encode(new_prod_log))

        # print(serializers.serialize("json", new_prod_log))
        # serializer = ProductHistorySerializer(new_prod_log, many=True)
        # return Response(serializer.data)
        # return Response(serializers.serialize("json", new_prod_log))
        return HttpResponse(jsondata, content_type="application/json")

    # for updating the quantity
    if request.method == 'POST':
        prod_row = ProductLog.objects.get(date=request.data['date'], time=request.data['time'], product_id=request.data['product_id'])
        old_qty = prod_row.quantity
        new_qty = request.data['quantity']
        print(prod_row.id)
        prod_row.quantity = new_qty
        prod_row.save()

        '''For Storing data in Master Log'''
        master_log_ser = MasterLogSerializer(data=request.data)
        master_log_ser.initial_data['item_id'] = request.data['product_id']
        master_log_ser.initial_data['item_log_id'] = prod_row.id
        master_log_ser.initial_data['item_type'] = "product"
        master_log_ser.initial_data['action'] = "UPDATE"
        master_log_ser.initial_data['date'] = datetime.now().today().strftime('%Y-%m-%d')
        master_log_ser.initial_data['time'] = datetime.now().today().strftime('%H:%M:%S')
        if master_log_ser.is_valid():
            master_log_ser.save()

        product = Products.objects.get(id=request.data['product_id'])
        prod_qty = product.quantity
        prod_qty = prod_qty - old_qty + new_qty
        product.quantity = prod_qty
        product.save()

        p_id = request.data['product_id']
        item_list = RawMaterialMapping.objects.filter(product_type_id=p_id)
        # product_qty = request.data['quantity']
        for item in item_list:
            no_of_parts = item.no_of_parts_used
            rm_id = item.raw_material_type_id
            raw_material = RawMaterial.objects.get(id=rm_id)
            raw_material.quantity = raw_material.quantity + (old_qty-new_qty) * no_of_parts
            if raw_material.item_name == 'Armature':
                arm_prod = Products.objects.get(product_name="Armature")
                arm_prod.quantity = raw_material.quantity
                arm_prod.save()
            raw_material.save()

        if request.data['product_id'] == 6:
            arm = RawMaterial.objects.get(item_name="Armature")
            arm.quantity = product.quantity
            arm.save()

        return Response(serializers.serialize("json", [prod_row]))


@api_view(['GET'])
def product_log_detail(request):

    try:
        prod_id = request.query_params.get('id')
        print(prod_id)
        product_log = ProductLog.objects.filter(product_id_id=prod_id)
    except ProductLog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductLogSerializer(product_log, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def raw_material_log_list(request):
    if request.method == 'GET':
        queryset = RawMaterialLog.objects.all()
        serializer = RawMaterialLogSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':                          # for updating the quantity
        raw_material_row = RawMaterialLog.objects.get(date=request.data['date'], time=request.data['time'], raw_material_id=request.data['raw_material_id'])
        old_qty = raw_material_row.quantity
        new_qty = request.data['quantity']

        raw_material_row.quantity = new_qty
        raw_material_row.save()

        '''For Storing data in Master Log'''
        master_log_ser = MasterLogSerializer(data=request.data)
        master_log_ser.initial_data['item_id'] = request.data['raw_material_id']
        master_log_ser.initial_data['item_log_id'] = raw_material_row.id
        master_log_ser.initial_data['item_type'] = "rawMaterial"
        master_log_ser.initial_data['action'] = "UPDATE"
        master_log_ser.initial_data['date'] = datetime.now().today().strftime('%Y-%m-%d')
        master_log_ser.initial_data['time'] = datetime.now().today().strftime('%H:%M:%S')
        if master_log_ser.is_valid():
            master_log_ser.save()

        raw_material = RawMaterial.objects.get(id=request.data['raw_material_id'])
        prod_qty = raw_material.quantity
        prod_qty = prod_qty - old_qty + new_qty
        raw_material.quantity = prod_qty
        raw_material.save()

        return Response(serializers.serialize("json", [raw_material_row]))


@api_view(['GET'])
def raw_material_log_detail(request):
    try:
        raw_mat_id = request.query_params.get('id')
        raw_material_log = RawMaterialLog.objects.filter(raw_material_id_id=raw_mat_id)
    except RawMaterialLog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RawMaterialLogSerializer(raw_material_log, many=True)
        return Response(serializer.data)














