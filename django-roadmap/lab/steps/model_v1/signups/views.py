from django.shortcuts import render

from .models import Dish


def dish_list(request):
    return render(request, "signups/list.html", {"dishes": Dish.objects.all()})
