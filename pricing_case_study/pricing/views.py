from django.core.cache import cache
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from .models import PriceData,UploadedFile
from rest_framework import status
from .tasks import process_csv_file
from .serializers import PriceDataSerializer
import os
import logging

# Create your views here.

logger = logging.getLogger('django')

import csv

import csv

def validate_csv(filename):
    expected_headers = ['Store ID', 'SKU', 'Product Name', 'Price', 'Date']
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader, None) 
        return headers == expected_headers
    



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    try:
        file = request.FILES['file']
        uploaded_file = UploadedFile.objects.create(file=file)
        file_path = uploaded_file.file.path
        logger.info(f"File {file.name} uploaded by user {request.user}.")
        if not file.name.endswith('.csv'):
           return Response({"error": "Only CSV files are allowed"}, status=status.HTTP_400_BAD_REQUEST)
        if not validate_csv(file_path):
            logger.info(f"Invalid CSV : {file.name}.")
            return Response({"error": "Invalid CSV : headers not matched"}, status=status.HTTP_400_BAD_REQUEST)
        process_csv_file.delay(file_path)
        logger.info(f"Processing started for file {file.name}.")
        return Response({"message": "File is being processed"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return Response({"error":"Failed to upload file"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_records(request):
    try:
        logger.info("Getting all records")
        cache_key = f"search_results_{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info("Serving data from cache")
            return Response(cached_data)
        
        queryset = PriceData.objects.all().order_by('id')

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = PriceDataSerializer(paginated_queryset, many=True)
        response_data = paginator.get_paginated_response(serializer.data)


        cache.set(cache_key, response_data.data, timeout=300)
        logger.info("Caching the search results.")

        return response_data

    except Exception as e:
        logger.error(f"Error fetching records: {e}")
        return Response({"error": "Failed to fetch records"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_record(request):
    try:
        store_id = request.GET.get('store_id','').strip()
        sku = request.GET.get('sku','').strip()
        name = request.GET.get('name','').strip()

        filters ={}
        logger.info(f"searching record .")
        if store_id :
            filters["store_id"] = store_id
        
        if sku :
            filters["sku"] = sku
        
        if name :
            filters["name__icontains"] =  name
        
        if not filters:
            return Response({"error":"No search_query found"},status=status.HTTP_404_NOT_FOUND)
        queryset = PriceData.objects.filter(**filters)
    
        if not queryset.exists():
            logger.warning("Record not found.")
            return Response({"error":"No match found"},status=status.HTTP_404_NOT_FOUND)
        serializer = PriceDataSerializer(queryset,many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error searching record : {e}")
        return Response({"error": "Failed to search record"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_record(request,pk):
    try:
        print("editing record ...")
        record = PriceData.objects.get(pk=pk)
        serializer = PriceDataSerializer(record,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Record {pk} updated by user {request.user}.")
            cache_key_prefix = "search_results_"
            cache_keys = cache.keys(f"{cache_key_prefix}*")  # Fetch all keys matching the prefix
            for key in cache_keys:
                cache.delete(key)
                logger.info(f"Cache invalidated for key: {key}")
            return Response(serializer.data)
        logger.warning(f"Validation errors while updating record {pk}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PriceData.DoesNotExist:
        logger.warning(f"Record {pk} not found.")
        return Response({"error":"Record not found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating record {pk}: {e}")
        return Response({"error": "Failed to update record"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

