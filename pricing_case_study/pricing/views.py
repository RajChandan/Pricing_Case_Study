from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from .models import PriceData,UploadedFile
from rest_framework import status
from .tasks import process_csv_file
from .serializers import PriceDataSerializer
import os

# Create your views here.

@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def upload_csv(request):
    file = request.FILES['file']
    uploaded_file = UploadedFile.objects.create(file=file)
    file_path = uploaded_file.file.path
    process_csv_file(file_path)
    return JsonResponse({"message":"File is being processed."})



@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def search_record(request):
    store_id = request.GET.get('store_id')
    sku = request.GET.get('sku')
    name = request.GET.get('name')

    filters ={}

    if store_id :
        filters["store_id"] = store_id
    
    if sku :
        filters["sku"] = sku
    
    if name :
        filters["name__icontains"] =  name
    
    print(store_id,sku,name)

    print(filters," -- filters")
    queryset = PriceData.objects.filter(**filters)

    if not queryset.exists():
        return JsonResponse({"error":"No match found"},status=status.HTTP_404_NOT_FOUND)
    serializer = PriceDataSerializer(queryset,many=True)
    return Response(serializer.data)