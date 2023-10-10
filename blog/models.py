from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField(auto_now=True)
    image = models.ImageField()
    body = models.TextField()

    def __str__(self):
        return self.title