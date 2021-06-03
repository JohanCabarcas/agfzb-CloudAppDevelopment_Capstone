from models import CarDealer, DealerReview

SEDAN = 'Sedan'
SUV = 'SUV'
WAGON = 'Wagon'
example = (SEDAN, 'Sedan'),
MODEL_CHOICES = [
    (SEDAN, 'Sedan'),
    (SUV, 'SUV'),
    (WAGON, 'Wagon'),
]

print("type {}".format(type(example)))

def car_model_getter():
    car_model = CarModel()
    return car_model

car = car_model_getter

print(car)

    <!--Add review form here -->
        <!--<form class="form-group" action="{% url 'djangoapp:add_review' dealer_id.dealer_id %}"  method="post">
            <textarea class="form-control" id="content" name="content" rows="2" required></textarea>
            <input class="form-check-input" type="checkbox" name="purchasecheck" id="purchasecheck"> 
            <select name="car" id="car" class="form-select" required>
                {% for car in cars %}
                    <option selected value={{car.id}}>{{car.name}}-{{car.make.name}}-{{ car.year|date:"Y" }}</option>
                {% endfor %}
            </select>
        </form>-->
