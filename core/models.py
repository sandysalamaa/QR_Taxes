from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sort_order = models.PositiveIntegerField(
        default=0,
        help_text="Control display order. Lower numbers appear first."
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Discount amount per item"
    )
    tax = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Tax amount per item"
    )
    scan_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='receipts/')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.merchant_name}"
    
class Item(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255) 
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New discount fields (matches your screenshot)
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Discount amount per item"
    )
    # Direct total price field (no calculation)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Final price after discounts (manually entered)"
    )
    # is_discount_applied = models.BooleanField(
    #     default=False,
    #     verbose_name="Discount Applied"  # Matches the checkmark in your screenshot
    # )

    # @property
    # def total_price(self):
    #     return (self.quantity * self.unit_price) - self.discount

    def __str__(self):
        return f"{self.name} x{self.quantity}"
