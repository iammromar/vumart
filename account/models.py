from tokenize import blank_re
from django.db import models
from account.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

from catalog.models import Product


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Telefon', unique=True, max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    telephone = models.CharField(max_length=128, null=True, blank=True)
    representer = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name='AKTİVDİR', default=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
        ordering = ('-id',)  # if you will change it, check generating random email function

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_name_field = self._meta.get_field('first_name')
        first_name_field.verbose_name = 'İstİfadəçİ  Adı'

        date_joined_field = self._meta.get_field('date_joined')
        date_joined_field.verbose_name = 'QEYDİYYAT TARİXİ'

    def __str__(self):
        return self.get_full_name()



    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def selected_address(self):
        address = self.addresses.filter(is_selected=True).last()
        if address:
            return address
        else:
            return False


class City(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
class Address(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    building = models.CharField(max_length=256, null=True, blank=True)
    apartment = models.CharField(max_length=256, null=True, blank=True)
    zip = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    lat = models.CharField(max_length=256, null=True, blank=True)
    lon = models.CharField(max_length=256, null=True, blank=True)
    note = models.CharField(max_length=256, null=True, blank=True)
    is_selected = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.name



class Wishlist(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name