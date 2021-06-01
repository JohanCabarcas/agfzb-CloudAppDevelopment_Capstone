from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'car_model_name', 'dealer_id')
    list_filter = ['car_model_name', 'car_make']
    search_fields = ['car_model_name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name_manufaturer', 'description')
    list_filter = ['name_manufaturer']
    search_fields = ['name_manufaturer']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
