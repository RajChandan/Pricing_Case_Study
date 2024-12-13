from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import AccessToken
from .models import PriceData

class ViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.access_token = str(AccessToken.for_user(self.user))
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

        self.price_data = PriceData.objects.create(
            store_id="1",
            sku="SKU123",
            name="Test Product",
            price=10.99,
            date="2024-06-10"
        )

        self.upload_url = reverse("upload_csv")  
        self.get_records_url = reverse("get_records") 
        self.search_url = reverse("search_record") 
        self.edit_record_url = reverse("edit_record", kwargs={"pk": self.price_data.pk}) 


    def test_upload_csv_valid(self):
        csv_content = b"Store ID,SKU,Product Name,Price,Date\n1,SKU123,Product1,20.00,2024-06-10"
        file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        response = self.client.post(self.upload_url, {"file": file}, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "File is being processed")

    def test_get_records(self):
        response = self.client.get(self.get_records_url,**self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())


    def test_search_record_valid(self):
        params = {"store_id": "1", "sku": "SKU123"}
        response = self.client.get(self.search_url, params,**self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_edit_record_valid(self):
        updated_data = {"name": "Updated Product Name", "price": 15.99}
        response = self.client.put(self.edit_record_url, updated_data, format="json",**self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Updated Product Name")
        self.assertEqual(float(response.json()["price"]), 15.99)

    
    def test_search_record_not_found(self):
        params = {"store_id": "999"}
        response = self.client.get(self.search_url, params)
        print(response.status_code,'status')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["error"], "No match found")