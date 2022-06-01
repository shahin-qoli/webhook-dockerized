
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from web.API.serializers import PriceListSerializer
from web.models import PriceLists, Prices


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pricelist_collection(request):
    if request.method == 'GET':
        price_list = PriceLists.objects.all()
        serializer = PriceListSerializer(price_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PriceListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pricelist_element(request, pk):
    try:
        price_list = PriceLists.objects.get(pk=pk)
    except PriceLists.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PriceListSerializer(price_list)
        return Response(serializer.data)
