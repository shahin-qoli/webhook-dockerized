from django.db import models
from django.contrib.auth.models import User

# CoreTable
class SpreeProducts(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    available_on = models.DateField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    tax_category_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    discontinue_on = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('id',)

# CoreTable
class SpreeVariants(models.Model):
    id = models.IntegerField(primary_key=True)
    sku = models.CharField(max_length=200)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_master = models.BooleanField()
    product = models.ForeignKey(SpreeProducts, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=200, decimal_places=0, blank=True, null=True)
    track_inventory = models.BooleanField()
    tax_category_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    discontinue_on = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.sku


# CoreTable
class SpreePrices(models.Model):
    id = models.IntegerField(primary_key=True)
    variant = models.ForeignKey(SpreeVariants, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=200, decimal_places=0)
    currency = models.CharField(max_length=200)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    compare_at_amount = models.DecimalField(max_digits=200, decimal_places=0, blank=True, null=True)


    def __int__(self):
        return self.variant_id


class SpreeOptionValues(models.Model):
    id = models.IntegerField(primary_key=True)
    position = models.IntegerField()
    name = models.CharField(max_length=200)
    presentation = models.CharField(max_length=200)
    option_type_id = models.IntegerField()

    def __str__(self):
        return self.name




# CoreTable
class Requests(models.Model):
    data = models.JSONField()
    event_created_at = models.DateTimeField()
    event_id = models.IntegerField(primary_key=True)
    event_type = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)


    def __int__(self):
        return self.event_id


class SpreeOptionValueVariants(models.Model):
    id = models.IntegerField(primary_key=True)
    variant = models.ForeignKey(SpreeVariants, on_delete=models.CASCADE)
    option_value = models.ForeignKey(SpreeOptionValues, on_delete=models.CASCADE)

    def __int__(self):
        return self.variant_id


class PriceHistory(models.Model):
    variant = models.ForeignKey(SpreeVariants, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=200, decimal_places=0)
    created_date = models.DateTimeField()
    price_date = models.DateTimeField(null=True)
    price_source = models.CharField(max_length=200,default=None)

    def __int__(self):
        return self.variant_id


class ExcelImport(models.Model):
    variant_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=200, decimal_places=0)
    price_date = models.CharField(max_length=200)
    import_title = models.CharField(max_length=200, default=None)
    def __int__(self):
        return self.variant_id

class Brands(models.Model):
    title = models.CharField(max_length=200)
    option_value = models.ForeignKey(SpreeOptionValues,unique=True, primary_key=True,on_delete= models.CASCADE)
    def __str__(self):
       return self.title

class PriceLists(models.Model):
        brand = models.ForeignKey(Brands, on_delete= models.CASCADE)
        title =  models.CharField(max_length=200)
        created_at = models.DateTimeField()
        created_by = models.ForeignKey(User,on_delete=  models.CASCADE,null= True, blank=True)
        start_at = models.DateField(null= True, blank= True)
        end_at = models.DateField(null= True, blank= True)
        retailer_discount = models.DecimalField(max_digits=200, decimal_places=3,null= True, blank= True)
        distributer_discount = models.DecimalField(max_digits=200, decimal_places=3,null= True, blank= True)
        retailer_cheque_discount = models.DecimalField(max_digits=200, decimal_places=3,null= True, blank= True)
        distributer_cheque_discount = models.DecimalField(max_digits=200, decimal_places=3,null= True, blank= True)
        cheque_time = models.IntegerField(null= True, blank= True)
        def __str__(self):
            return self.title


class Prices(models.Model):
        PriceLists = models.ForeignKey(PriceLists, on_delete=models.CASCADE)
        variant = models.ForeignKey(SpreeVariants, on_delete=models.CASCADE)
        price = models.IntegerField(null= True, blank=True)
        retailer_price = models.IntegerField(null= True, blank=True)
        distributer_price = models.IntegerField(null= True, blank=True)
        def __int__(self):
           return self.variant_id


