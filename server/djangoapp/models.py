#from django.db import models

# Create your models here.

#************************Settings*************************#
import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

# <HINT> Create a Car Make model `
class CarMake(models.Model):
    name_manufaturer = models.CharField(null=False, max_length=30, default='manufaturer')
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return "Manufacturer: " + self.name_manufaturer + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `
class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
# - Name
    car_model_name = models.CharField(null=False, max_length=30, default='car_model')
# - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField(default=0)
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'

    MODEL_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    choice = models.CharField(
        null=False,
        max_length=20,
        choices=MODEL_CHOICES,
        default=SEDAN
    )

# - Year (DateField)
    year = models.DateField(null=True)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
    def __str__(self):
        return "Manufacturer: " + self.car_make.name_manufaturer + "," + \
                "Car model: " + self.car_model_name + "," + \
                "Car choice: " + self.choice + "," + \
                "Year: " + str(self.year)[:10]

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, state, st):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Dealer state
        self.state = state
        #Dealer state short
        self.st = st

    def __str__(self):
        return "Dealer name: " + self.full_name



# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview :
    def __init__(self, dealership, name, review, car_model, purchase, sentiment="default"):
        # Dealer address
        self.dealership = dealership
        # Dealer city
        self.name = name
        # Dealer Full Name
        self.review = review
        # Dealer id
        self.car_model = car_model
        # Purchase
        self.purchase = purchase
        #Sentiment result NLU
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review + "," + \
                "Car model" + self.car_model
