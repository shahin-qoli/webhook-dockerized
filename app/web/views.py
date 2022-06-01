import io
import json
from datetime import datetime
from jalali_date import datetime2jalali, date2jalali
from threading import Thread


import pandas

from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, inlineformset_factory, formset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import xlwt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import ListView, DetailView

from sqlalchemy import create_engine

from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *


@csrf_exempt

def getDataFromSpree(request):
    if request.method == 'GET':
        print('get')
    elif request.method == 'POST':
        bresbody = request.body
        fix_bytes_value = bresbody.replace(b"'", b'"')
        my_json = json.load(io.BytesIO(fix_bytes_value))
        # resbody = bresbody.decode('utf8')
        # resbody = resbody.replace()
        Requests.objects.create(data=my_json['data'], event_type=my_json['event_type'],
                                event_created_at=my_json['event_created_at'], event_id=my_json['event_id'])
        t = Thread(target=processNewRecord)
        t.start()
    response = HttpResponse(status=200)
    return response


def processNewRecord():
    undoneq = Requests.objects.filter(is_done=False)
    price_source = "Spree"
    for un in undoneq:
        if un.event_type == 'price.update':
            Requests.objects.filter(event_id=un.event_id).update(is_done=True)
            priceUpdateFromWebhook(un.data, price_source)


def priceUpdateFromWebhook(data, price_source):
    variant_id = int(data['id'])
    attributes = data['attributes']
    new_price = attributes['amount']
    update_date = attributes['updated_at']
    variant = SpreeVariants.objects.get(id=variant_id)
    PriceHistory.objects.create(variant=variant, amount=new_price, created_date=update_date, price_date=update_date,
                                price_source=price_source)
    SpreePrices.objects.filter(variant_id=variant_id).update(amount=new_price, updated_at=update_date)


@login_required
@csrf_exempt
def pageIndex(request):
    if request.method == 'GET':
        rule_list = []
        brands = SpreeOptionValues.objects.filter(option_type_id=1)
        # for rule in rules:
        #   rule_list.append(rule.title)
        return render(request, "web/index.html", {"brands": brands})
    elif request.method == 'POST':
        pass


@login_required
def templateImport(request):
    if request.method == 'POST':
        file = request.FILES['file']
        df = pandas.read_excel(file, 'Prices')
        engine = create_engine('postgresql://postgres:@localhost:5432/SpreeWebhook')
        df['title'] = request.POST['title']
        df['is_done'] = False
        df.to_sql('web_excelimport_2', engine, if_exists='append')
        response = priceUpdateFromExcel(df)
        message = "ok"
        return response
        return render(request, 'web/message.html', {"message": message})

    else:
        form = UploadFileForm()
    return render(request, 'web/uploadfile.html', {'form': form})


def templateExport(request, value):
    if request.method == 'GET':
        optn_vlue_variants = helperBrandVariants(value)
        rows = []
        for so in optn_vlue_variants:
            pn = so['product_name']
            pb = so['product_brand']
            vi = so['variant_id']
            tuple = (vi, pn, pb, None, None)
            rows.append(tuple)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Template.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Prices')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['VariantId', 'ProductName', 'Brand', 'Price', 'PriceDate', ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response


def helperBrandVariants(value):
    vrints = SpreeVariants.objects.filter(spreeoptionvaluevariants__option_value__id=value)
    optn_vlue_variants = []
    for var in vrints:
        product_name = SpreeProducts.objects.get(spreevariants__id=var.id).name
        product_brand = SpreeOptionValues.objects.get(id=value).name
        data = {"product_name": product_name, "product_brand": product_brand, "variant_id": var.id,
                "variant_sku": var.sku}
        optn_vlue_variants.append(data)
    return optn_vlue_variants


def priceUpdateFromExcel(df):
    df['Status'] = 'ok'
    for i in range(len(df.index)):

        vaid = int(df['VariantId'][i])
        amount = int(df['Price'][i])
        variant = SpreeVariants.objects.get(id=vaid)
        try:
            PriceHistory.objects.create(variant=variant, amount=amount, created_date=datetime.now(),
                                        price_date=datetime.now(), price_source="excel")
        except:
            df['Status'][i] = 'error'

    response = resultExport(df)
    return response


def resultExport(df):
    rows = []

    for i in range(len(df.index)):
        VariantId = int(df['VariantId'][i])
        tuple = (
        df['VariantId'][i], df['ProductName'][i], df['Brand'][i], df['Price'][i], df['PriceDate'][i], df['Status'][i])
        rows.append(tuple)
    ###yadat bashad maghrooor nashavi
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Template.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Prices')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['VariantId', 'ProductName', 'Brand', 'Price', 'PriceDate', 'Status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response


"""class PriceListView(ListView):
    queryset = PriceLists.objects.all()
    context_object_name = 'pricelists'
"""


class BrandListView(ListView):
    queryset = Brands.objects.all()
    context_object_name = 'brands'


class BrandDetailsView(ListView):
    template_name = 'books/brands_detail.html'
    context_object_name = 'pricelist'

    def get_queryset(self):
        self.pricelist = PriceLists.objects.filter(brand_id=self.kwargs['id'])


class PriceListView(ListView):

    context_object_name = 'pricelist'

    def get_queryset(self):
        self.brand = get_object_or_404(Brands, option_value_id=self.kwargs['brand_id'])
        return PriceLists.objects.filter(brand=self.brand)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_id'] = self.kwargs['brand_id']
        return context






def pagePriceListDetails(request, pk):
    prices = Prices.objects.filter(PriceLists_id=pk)
    pr_list = []
    price_formset = formset_factory(priceForm)
    queryset= PriceLists.objects.get(id=pk)
    header_list = {'brand' : queryset.brand, 'title' : queryset.title, 'created_at' : queryset.created_at ,'created_by' : queryset.created_by ,'start_at': queryset.start_at ,'end_at' : queryset.end_at ,'retailer_discount': queryset.retailer_discount, 'distributer_discount' : queryset.distributer_discount ,'retailer_cheque_discount': queryset.retailer_cheque_discount ,'distributer_cheque_discount': queryset.distributer_cheque_discount , 'cheque_time': queryset.cheque_time      }
    form = priceListForm(initial=header_list)

    for pr in prices:
        product_title = SpreeProducts.objects.get(spreevariants__id=pr.variant_id).name
        price = pr.price
        retailer_price = pr.retailer_price
        distributer_price = pr.distributer_price
        variant_id = pr.variant_id
        list = ({'product_title': product_title, 'variant_id': variant_id, 'price': price, 'retailer_price': retailer_price,
                'distributer_price': distributer_price, })
        pr_list.append(list)
    formset = price_formset(initial=pr_list)
    return render(request,'web/ui/pricelist_view.html', {'form' : form, 'formset': formset})

@login_required
def pagePriceListCreate(request,brand_id):


    brand = Brands.objects.get(option_value_id=brand_id)
    user = request.user

    price_formset = formset_factory(priceForm)
    #pricelist_formset = pricelist_formset(initial= var_list )
    if request.method == 'GET':
        header_form = priceListForm({'brand': brand})

       # formset = price_formset(initial=var_list)
        return render(request,'web/ui/price_list_create.html', {'form' : header_form})
    elif request.method == 'POST':
        header_form = priceListForm(request.POST, {'brand': brand, 'created_by': user})
        if header_form.is_valid():
           PriceLists.objects.create(brand= brand, title= request.POST['title'],created_at=request.POST['created_at'],created_by= user,start_at=request.POST['start_at'],end_at=request.POST['end_at'],retailer_discount=request.POST['retailer_discount'],distributer_discount=request.POST['distributer_discount'],retailer_cheque_discount=request.POST['retailer_cheque_discount'],distributer_cheque_discount=request.POST['distributer_cheque_discount'],cheque_time=request.POST['cheque_time'])
           new_price_list_pk = PriceLists.objects.latest('id')
           return pagePriceCreateReady(request,new_price_list_pk,brand_id)
        else:
          print("not OK")
@login_required
def pagePriceCreateReady(request,pk,brand_id):
    price_formset = formset_factory(priceForm,extra=0)
    pr_list = []
    products = SpreeProducts.objects.filter(spreevariants__spreeoptionvaluevariants__option_value_id__exact=brand_id,
                                            spreevariants__sku__istartswith='PL').order_by().values('name',
                                                                                                       'id', ).distinct()
    for pr in products:
        product_title = pr['name']
        variant_id = SpreeVariants.objects.get(is_master=True, product_id=pr['id']).id
        list = (
            {'product_title': product_title, 'variant_id': variant_id, })
        pr_list.append(list)
    if request.method == 'POST':
        formset= price_formset(request.POST,initial=pr_list)
        if formset.is_valid():
            Prices.objects.create(PriceLists_id= pk,variant_id= request.POST['variant_id'] ,price= request.POST['price'],retailer_price=request.POST['retailer_price'],distributer_price=request.POST['distributer_price'])

    brand_a = Brands.objects.get(option_value_id=brand_id)
    formset = price_formset(initial=pr_list)
    return render(request,'web/ui/prices_create.html', {'formset': formset,'pk' : pk, 'brand_id': brand_id, 'brand_a': brand_a})
@login_required
def pagePriceCreate(request,brand_id,pk):
    price_formset = formset_factory(priceForm,extra=0)
    pr_list = []
    products = SpreeProducts.objects.filter(spreevariants__spreeoptionvaluevariants__option_value_id__exact=brand_id,
                                            spreevariants__sku__istartswith='PL-').order_by().values('name',
                                                                                                       'id', ).distinct()

    for pr in products:
        product_title = pr['name']
        variant_id = SpreeVariants.objects.get(is_master=True, product_id=pr['id']).id
        list = (
            {'product_title': product_title, 'variant_id': variant_id,'price' : 0,'retailer_price' : 0, 'distributer_price' : 0 })
        pr_list.append(list)
    if request.method == 'POST':
        formset= price_formset(request.POST, initial=pr_list)
        if formset.is_valid():
          for form in formset:
              if form.cleaned_data['price'] == None:
                  pass
              else:
                  Prices.objects.create(PriceLists_id= pk,variant_id= form.cleaned_data['variant_id'] ,price= form.cleaned_data['price'],retailer_price=form.cleaned_data['retailer_price'],distributer_price=form.cleaned_data['distributer_price'])
        return pagePriceListDetails(request,pk)
        formset.error_messages
        print(formset.errors)
        print(formset.errors)

@login_required
def pageTest(request):
    form = test
    data = [{"title" : "sal1", "id" : 1},{"title" : "sal2", "id" : 2}]
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render(request, 'web/test.html', {'form' : form, 'data': data})

@login_required
def pageExcelHome(request):
    if request.method == 'GET':
        rule_list = []
        brands = SpreeOptionValues.objects.filter(option_type_id=1)
        # for rule in rules:
        #   rule_list.append(rule.title)
        return render(request, "web/excel/index.html", {"brands": brands})
    elif request.method == 'POST':
        pass
@login_required
def pageFormHome(request):
    if request.method == 'GET':
      pass