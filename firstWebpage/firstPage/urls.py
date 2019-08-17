'''from .api import StockApi
from django.conf.urls import url

urlpatterns=[
    url(r'^home/stocks$', StockApi.as_view())
]'''
from django.conf.urls import url
from firstPage import api
# from .api import RawMaterialViewSet
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'stocks', RawMaterialViewSet)
'''router.register(r'products', ProductViewSet)'''

urlpatterns = [url(r'^products/$', api.product_list),
               url(r'^products/(?P<pk>[0-9]+)/$', api.product_detail),
               url(r'^product/rawMaterial$', api.get_raw_materials_for_product),

               url(r'rawMaterial/$', api.stocks_list),
               url(r'^rawMaterial/(?P<pk>[0-9]+)/$', api.stock_detail),

               url(r'productLog/$', api.product_log_list),
               url(r'^productLog/specific/$', api.product_log_detail),


               url(r'^rawMaterialLog/$', api.raw_material_log_list),
               url(r'^rawMaterialLog/specific/$', api.raw_material_log_detail),

               url(r'^products/saleHistory/$', api.get_sale_history)]


# urlpatterns += router.urls

