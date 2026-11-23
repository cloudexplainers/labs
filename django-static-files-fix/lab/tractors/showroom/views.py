from django.shortcuts import render

TRACTORS = [
    {"name": "Field Star 45", "hp": 45, "price": "$31,900", "img": "img/field-star.svg"},
    {"name": "Hill Hauler 60", "hp": 60, "price": "$42,500", "img": "img/hill-hauler.svg"},
    {"name": "Orchard Mini 25", "hp": 25, "price": "$18,750", "img": "img/orchard-mini.svg"},
]


def home(request):
    return render(request, "showroom/home.html", {"tractors": TRACTORS})
