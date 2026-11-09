from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Tea


def tea_list(request):
    teas = Tea.objects.order_by("name")
    return render(request, "shop/tea_list.html", {"teas": teas})


def tea_detail(request, slug):
    tea = get_object_or_404(Tea, slug=slug)
    return render(request, "shop/tea_detail.html", {"tea": tea})


def order(request, slug):
    tea = get_object_or_404(Tea, slug=slug)
    form = OrderForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data["quantity"] > tea.stock:
            form.add_error("quantity", f"Only {tea.stock} left in stock.")
        else:
            new_order = form.save(commit=False)
            new_order.tea = tea
            new_order.save()
            return redirect("thanks")
    return render(request, "shop/order.html", {"tea": tea, "form": form})


def thanks(request):
    return HttpResponse("Thank you! Your order is in.")
