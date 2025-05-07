from django.urls import path

from kitchen.views import (
    index,
    DishListView,
    DishDetailView,
    DishTypeListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type-list")
]

app_name = "kitchen"
