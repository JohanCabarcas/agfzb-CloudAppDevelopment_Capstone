from .models import CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request
import requests

url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/dealership"
# Get dealers from the URL
dealerships = get_dealers_from_cf(url)
    # Map cardealer obj list to context dict        
for dealership in dealerList:
    for row in dealership:
        context["address"] = row.address
        context["city"] = row.city
        context["full_name"] = row.full_name
        context["id"] =row.id
        context["st"] = row.st
        context["state"] = row.state
print("OCntext dict {}".format(context))
# Concat all dealer's short name
dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
# Return a list of dealer short name

