from django.shortcuts import redirect, render

from .forms import DishForm
from .models import Dish


def dish_list(request):
    return render(request, "signups/list.html", {"dishes": Dish.objects.all()})


def sign_up(request):
    form = DishForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("/signups/")
    return render(request, "signups/new.html", {"form": form})
