from django.core.validators import MinValueValidator
from django.db import models


class Tea(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    tea = models.ForeignKey(Tea, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
