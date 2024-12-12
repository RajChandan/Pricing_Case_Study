from django.core.cache import cache
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
import logging

# Create your views here.

logger = logging.getLogger('django')

@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def upload_csv(request):
    try:
        file = request.FILES['file']
        uploaded_file = UploadedFile.objects.create(file=file)
        file_path = uploaded_file.file.path
        logger.info(f"File {file.name} uploaded by user {request.user}.")
        process_csv_file.delay(file_path)
        logger.info(f"Processing started for file {file.name}.")
        return JsonResponse({"message":"File is being processed."})
    except Exception as e:
        print(e)
        logger.error(f"Error uploading file: {e}")
        return JsonResponse({"error":"Failed to upload file"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def get_records(request):
    try:
        logger.info("Getting all records")
        cache_key = f"search_results_{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("serving data from cache")
            return Response(cached_data)
        queryset = PriceData.objects.all()
        serializer = PriceDataSerializer(queryset,many=True)

        cache.set(cache_key, serializer.data, timeout=300)
        logger.info("Caching the search results.")

        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching record : {e}")
        return Response({"error": "Failed to fetch record"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def search_record(request):
    try:
        store_id = request.GET.get('store_id')
        sku = request.GET.get('sku')
        name = request.GET.get('name')

        filters ={}
        logger.info(f"searching record .")
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
            logger.warning("Record not found.")
            return JsonResponse({"error":"No match found"},status=status.HTTP_404_NOT_FOUND)
        serializer = PriceDataSerializer(queryset,many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error searching record : {e}")
        return Response({"error": "Failed to search record"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def edit_record(request,pk):
    try:
        record = PriceData.objects.get(pk=pk)
        serializer = PriceDataSerializer(record,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Record {pk} updated by user {request.user}.")
            return Response(serializer.data)
        logger.warning(f"Validation errors while updating record {pk}.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except PriceData.DoesNotExist:
        logger.warning(f"Record {pk} not found.")
        return Response({"error":"Record not found"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating record {pk}: {e}")
        return Response({"error": "Failed to update record"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
