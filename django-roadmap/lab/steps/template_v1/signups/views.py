from django.shortcuts import render


def dish_list(request):
    return render(request, "signups/list.html", {"dishes": []})
