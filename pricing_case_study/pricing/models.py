from django.db import models

# Create your models here.
class PriceData(models.Model):
    store_id = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} :: {self.store_id} :: {self.sku} :: {self.price} :: {self.date}"
    

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} :: {self.uploaded}"