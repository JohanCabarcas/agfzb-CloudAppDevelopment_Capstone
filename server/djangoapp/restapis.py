import requests
import json
from .models import CarDealer, DealerReview, CarModel
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("kwargs: {}".format(kwargs))
    #url = url + kwargs
    print("GET from {} ".format(url))

    #NLU api key
    #API_KEY = oW_diMKZmx3hlbpU8KVFYJN3fEpYWifB2YQu00sc0Yhr

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data        


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
# e.g., response = requests.post(url, params=kwargs, json=payload)
    response = requests.post(url, params=kwargs, json=json_payload)
    return response



# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list'''
    results = []
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url)
    except:
        # If any error occurs
        print("Network exception occurred")
        
    status = response.status_code
    print("With status {} ".format(status))
        
    json_result = json.loads(response.text)
    #print("The response get dealership {}".format(json_data))
    if json_result:
        # Get the row list in JSON as dealers
        #DEBUG print("json result {}".format(json_result))
        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            try:
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                        id=dealer_doc["id"],st=dealer_doc["st"], state=dealer_doc["state"])
                results.append(dealer_obj)
            except:
                print("i am an empty row")
        return results
        

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    print("********start get_dealer_by_id_from_cf***********")
    results = []
    # Call get_request with URL query dealer ID, get reviews according to dealer ID
    json_result = get_request(url)
    
    ###DEBUG
    print("JSON Results req {}".format(json_result))

    if json_result:
        # Get the row list in JSON as dealers
        review_dealers_id = json_result["docs"]

        ##DEBUG
        #print("JSON after appploy docs string {}".format(review_dealers_id))
        # For each dealer object
        for dealer_doc in review_dealers_id:
            review_analysis = dealer_doc["review"]
            print("Review for NLU {}".format(review_analysis))
            #NLU analyzer
            sentiment_res = analyze_review_sentiments(review_analysis)
            print("Sentiment result review {}".format(sentiment_res))

            dealer_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], review=dealer_doc["review"],
                        car_model=dealer_doc["car_model"], purchase=dealer_doc["purchase"], sentiment=sentiment_res)

            results.append(dealer_obj)

    print("********End get_dealer_by_id_from_cf***********")
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    API_KEY = "oW_diMKZmx3hlbpU8KVFYJN3fEpYWifB2YQu00sc0Yhr"
    NLU_URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ea9ec473-30f1-4cfe-8be9-ad4525d798f5/v1/analyze?version=2020-08-01"

    params = dict()
    params["text"] = text
    params["features"] = {"sentiment":{"document":True}}
    params["language"] = "en"

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(NLU_URL, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey',API_KEY),
                                    params=params)
    except:
        print("Cannot get a response from NLU request")
    #Log response params        
    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)

    sentiment_res = json_data["sentiment"]["document"]["label"]
    #print("the result {} ".format(sentiment_res))

    return sentiment_res

def car_model_getter():
    car = CarModel()
    print(car)
    #return car_model 





