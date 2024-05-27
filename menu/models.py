from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    catname = models.CharField(max_length=100)
    catimage = models.ImageField(upload_to='category')

    def __str__(self):
        return self.catname

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    detail = models.CharField(max_length=300)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class ProductClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} clicked at {self.timestamp}"

    def save(self, *args, **kwargs):
        self.product.click_count += 1
        self.product.save()
        super(ProductClick, self).save(*args, **kwargs)

class Logo(models.Model):
    image = models.ImageField(upload_to='logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Logo uploaded at {self.uploaded_at}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} {self.surname} - {self.email}"