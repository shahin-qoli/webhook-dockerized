from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views,initials
from .API.views import pricelist_collection, pricelist_element
from .importFromExcel import PriceList, Price, Brand

from .views import PriceListView, BrandDetailsView, BrandListView, pagePriceListDetails, \
     pageExcelHome, pagePriceListCreate, pageTest, pageFormHome, pagePriceCreateReady,pagePriceCreate


app_name = 'web'
urlpatterns = [
     path('hook/start/',views.getDataFromSpree,name='getdata'),
     path('init/spreeprices', initials.initSpreePrices, name='initSpreePrices'),
     path('init/spreeproducts', initials.initSpreeProducts, name='initSpreeProducts'),
     path('init/spreevariants', initials.initSpreeVariants, name='initSpreeVariants'),
     path('init/SpreeOptionValues', initials.initSpreeOptionValues, name='initSpreeOptionValues'),
     path('init/SpreeOptionValueVariants', initials.initSpreeOptionValueVariants, name='initSpreeOptionValueVariants'),
     path('', views.pageIndex, name='pageIndex'),
     path('price/export/<int:value>', views.templateExport, name='templateExport'),
     path('price/insert', views.templateImport, name= 'templateImport'),
     #path('list/pricelists/', PriceListView.as_view(), name="priceListView"),
     #path('list/brands/', BrandListView.as_view(), name="brandsListView"),
     path('form/brands/<brand_id>', PriceListView.as_view(), name="priceListView"),
     #path('list/pricelist/<int:pk>', PriceListListView.as_view(), name= "priceListDetailView")
     path('form/pricelist/<int:pk>', pagePriceListDetails, name="pagePriceListDetails"),
     path('list/pricelist/create/<brand_id>', pagePriceListCreate, name="pagePriceListCreate"),
     path('test/', pageTest, name="pageTest"),
     path('excel/', pageExcelHome, name= 'pageExcelHome'),
     path('form/', BrandListView.as_view(), name= 'pageFormHome'),
     path('forms/pricelist/prices/createReady', pagePriceCreateReady, name="pagePriceCreateReady"),
     path('forms/pricelist/prices/create/<brand_id>/<pk>', pagePriceCreate, name="pagePriceCreate"),
     path('init/excel/PriceList', PriceList, name="initPriceList"),
     path('init/excel/Price', Price, name="initPrice"),
     path('init/excel/Brand', Brand, name="initBrand"),


     #API
     path('api/v1/pricelists/', pricelist_collection),
     path('api/v1/pricelists/<pk>', pricelist_element),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]