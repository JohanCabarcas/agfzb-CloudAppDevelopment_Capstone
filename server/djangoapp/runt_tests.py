
import requests
import json
#from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code#
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
     def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

        results = []
        # Call get_request with a URL parameter
        json_result = get_request(url)
        if json_result:
            # Get the row list in JSON as dealers
            dealers = json_result["rows"]
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)

        return results
    return json_data


#get dealership table
#url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/dealership"

#Get dealership by State abreviation "St"
#url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/dealership/dealership?st=CA"

#Get dealership by id
url ="https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/reviews/reviews?dealership=15"
##Make request
json_data = get_request(url)

#def print_json (self,**kwargs):
#    for key, value in kwargs.items():
#        print ("%s == %s" %(key, value))

#print_json()