from django.shortcuts import render

from .models import Tea


def tea_list(request):
    teas = Tea.objects.order_by("name")
    return render(request, "shop/tea_list.html", {"teas": teas})
