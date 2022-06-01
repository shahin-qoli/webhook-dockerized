from rest_framework import serializers
from web.models import PriceLists, Prices, SpreeVariants, Brands


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('variant', 'price', 'retailer_price', 'distributer_price', )
        extra_kwargs = {'variant_id': {'write_only': True}}

class PriceListSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True,source='prices_set')

    class Meta:
        model = PriceLists
        fields = ('brand', 'title', 'created_at', 'created_by', 'start_at', 'end_at',
                  'retailer_discount', 'distributer_discount', 'retailer_cheque_discount',
                  'distributer_cheque_discount', 'cheque_time','prices',)
    extra_kwargs = {'brand_id': {'write_only': True}}

    def create(self, validated_data):
        prices_data = validated_data.pop('prices_set')
        price_list = PriceLists.objects.create(**validated_data)
        for price_data in prices_data:
            Prices.objects.create(PriceLists=price_list, **price_data)
        return price_list
