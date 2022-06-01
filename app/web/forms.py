from django import forms

from tempus_dominus.widgets import DatePicker




class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class test(forms.Form):
    test_title = forms.CharField(max_length=50)
    test_id = forms.IntegerField()
    number = forms.IntegerField()


class priceImportFromForm(forms.Form):
    variant_id = forms.IntegerField()
    product_name = forms.CharField(label='name')
    product_brand = forms.CharField(label='brand')
    product_price = forms.DecimalField(label='price')
    price_date = forms.DateField(label="date", widget=DatePicker())


class priceForm(forms.Form):
    variant_id = forms.IntegerField(label='variant_id')
    product_title = forms.CharField(label='product_title')
    price = forms.IntegerField(label="price",required=False)
    retailer_price = forms.IntegerField(label='retailer_price', required=False)
    distributer_price = forms.IntegerField(label="distributer_price", required=False)





class priceListForm(forms.Form):
    brand = forms.CharField(label='pricelist_brand' )
    title = forms.CharField(label='pricelist_title')
    created_at = forms.DateField()
#    created_by= forms.DateField()
    start_at= forms.DateField(widget=forms.SelectDateWidget())
    end_at= forms.DateField(widget=forms.SelectDateWidget())
    retailer_discount = forms.IntegerField()
    distributer_discount= forms.IntegerField()
    retailer_cheque_discount= forms.IntegerField()
    distributer_cheque_discount= forms.IntegerField()
    cheque_time= forms.IntegerField()


