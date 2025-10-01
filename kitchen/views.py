from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import CookCreationForm, CookUpdateForm, DishForm
from kitchen.models import Dish, DishType, Cook


@login_required
def index(request):
    context = {
        "num_dishes": Dish.objects.count(),
        "num_dish_types": DishType.objects.count(),
        "num_cooks": Cook.objects.count(),
        "latest_dishes": Dish.objects.select_related(
            "dish_type"
        ).order_by("-pk")[:5],
    }
    return render(request, "kitchen/index.html", context)


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "kitchen/dish_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        search = self.request.GET.get("search")
        if search:
            return queryset.filter(name__icontains=search)
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.prefetch_related("cooks")
    template_name = "kitchen/dish_detail.html"

    def post(self, request, *args, **kwargs):
        dish = self.get_object()
        if request.POST.get("action") == "delete":
            dish.cooks.remove(request.user)
        else:
            dish.cooks.add(request.user)
        return redirect("kitchen:dish-detail", pk=dish.pk)


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_delete_confirm.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 5
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"

    def get_queryset(self):
        queryset = DishType.objects.order_by("name")
        search = self.request.GET.get("search")
        if search:
            return queryset.filter(name__icontains=search)
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_delete_confirm.html"
    context_object_name = "dish_type"
    success_url = reverse_lazy("kitchen:dish-type-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        search = self.request.GET.get("search")
        if search:
            return queryset.filter(username__icontains=search)
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"
    queryset = Cook.objects.prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_delete_confirm.html"
    success_url = reverse_lazy("kitchen:cook-list")
