import asyncio
import time

from django.http import JsonResponse

from .models import Tea


def list_teas(request):
    teas = Tea.objects.values("name", "price", "stock")
    return JsonResponse(list(teas), safe=False)


def supplier(request):
    time.sleep(1)  # wait for the supplier's site
    return JsonResponse({"ok": True})


async def supplier_async(request):
    await asyncio.sleep(1)  # wait for the supplier's site
    return JsonResponse({"ok": True})
