from django.shortcuts import render
from django.views import generic

from kitchen.models import Dish, DishType


def index(request):
    return render(request, "kitchen/index.html")


class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
