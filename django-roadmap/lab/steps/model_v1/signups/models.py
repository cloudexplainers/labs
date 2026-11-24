from django.db import models


class Dish(models.Model):
    KINDS = [("main", "main"), ("side", "side"), ("dessert", "dessert")]
    name = models.CharField(max_length=60, unique=True)
    person = models.CharField(max_length=60)
    kind = models.CharField(max_length=10, choices=KINDS)

    def __str__(self):
        return self.name
