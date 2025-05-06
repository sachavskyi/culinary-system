from django.urls import path

from kitchen.views import (
    index,
    DishListView,
    DishDetailView,
)


urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail")
]

app_name = "kitchen"
