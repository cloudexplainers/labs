from django.db import models


class Tea(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
