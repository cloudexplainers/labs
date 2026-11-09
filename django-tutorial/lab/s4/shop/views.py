from django.shortcuts import get_object_or_404, render

from .models import Tea


def tea_list(request):
    teas = Tea.objects.order_by("name")
    return render(request, "shop/tea_list.html", {"teas": teas})


def tea_detail(request, slug):
    tea = get_object_or_404(Tea, slug=slug)
    return render(request, "shop/tea_detail.html", {"tea": tea})
