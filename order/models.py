from django.db import models
from django.contrib.auth import get_user_model

from account.models import Address
from catalog.models import Product

User = get_user_model()



class Payment(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ("PE", "Gözləmədə"),
        ("PR", "İşlənilir"),
        ("SP", "Yoldadır"),
        ("DL", "Çatdırıldı"),
        ("CL", "Ləğv edildi"),
    )
    is_ordered = models.BooleanField(default=False)
    ordered_date_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    note = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, default="PE", choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name}'

    @property
    def get_cart_total(self):
        orderitems = self.items.all()
        total = 0
        if orderitems:
            try:
                total = sum([item.total_price for item in orderitems]) - self.discount
            except:
                total = 0
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2,default=0)

    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        self.unit_price = self.product.prices.last().price
        self.total_price = self.product.prices.last().price * self.quantity - self.discount

        super(OrderItem, self).save(*args, **kwargs)
