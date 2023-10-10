from django.db import models

class Subscription(models.Model):
    email = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.email

class Country(models.Model):
    name = models.CharField(max_length=256)
    flag = models.ImageField()

    def __str__(self):
        return self.name


class General(models.Model):
    logo = models.ImageField()
    address = models.CharField(max_length=256)
    address_url = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    topbar_text = models.TextField()
    copyright = models.CharField(max_length=256)
    footer_payment_image = models.FileField()

    def __str__(self):
        return f'Ümumi məlumatlar'
