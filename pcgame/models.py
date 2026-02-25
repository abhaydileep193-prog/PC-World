from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Desktop', 'Desktop PC'),
        ('CPU', 'Processor'),
        ('GPU', 'Graphics Card'),
        ('RAM', 'Memory'),
        ('SSD', 'Storage'),
        ('Motherboard', 'Motherboard'),
        ('PSU', 'Power Supply'),
        ('Cabinet', 'Cabinet'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.get_name_display()

class PCProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='pc_products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} ({self.brand})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('PCProduct', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

image = models.ImageField(upload_to="pc_products/", blank=True, null=True)