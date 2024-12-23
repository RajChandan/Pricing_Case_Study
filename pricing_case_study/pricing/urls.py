from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.get_records, name='get_records'), 
    path('upload/', views.upload_csv, name='upload_csv'),
    path('search/', views.search_record, name='search_record'), 
    path('records/<int:pk>/', views.edit_record, name='edit_record'),  
]