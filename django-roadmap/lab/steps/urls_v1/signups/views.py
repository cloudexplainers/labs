from django.http import HttpResponse


def dish_list(request):
    return HttpResponse("Potluck sign-ups: no dishes yet")
