from django.db import models



class Country(models.Model):
    name = models.CharField(max_length=256)
    flag = models.ImageField()

    def __str__(self):
        return self.name
