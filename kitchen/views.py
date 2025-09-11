from django.shortcuts import render
from django.views import generic

from kitchen.models import Dish, DishType, Cook


def index(request):
    context = {
        "num_dishes": Dish.objects.count(),
        "num_dish_types": DishType.objects.count(),
        "num_cooks": Cook.objects.count(),
    }
    return render(request, "kitchen/index.html", context)


class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class CookListView(generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"


class CookDetailView(generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"
