from django.contrib import admin

from kitchen.models import Cook, Dish, DishType


admin.site.register(Dish)
admin.site.register(DishType)
admin.site.register(Cook)
