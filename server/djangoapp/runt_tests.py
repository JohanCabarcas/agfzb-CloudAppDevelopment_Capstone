import requests
import json
#from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    API_KEY = "oW_diMKZmx3hlbpU8KVFYJN3fEpYWifB2YQu00sc0Yhr"
    NLU_URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ea9ec473-30f1-4cfe-8be9-ad4525d798f5/v1/analyze?version=2020-08-01"

    params = dict()
    params["text"] = text
    #params["version"] = '2020-08-01'
    params["features"] = {"sentiment":{"document":True}}
    params["language"] = "en"
    #params["return_analyzed_text"] = kwargs["return_analyzed_text"]

    print("the params {}".format(params))
    #print("the kwargs {}".format(kwargs))

    #response = requests.get(NLU_URL, params=params, headers={'Content-Type': 'application/json'},
    #                                auth=HTTPBasicAuth('apikey', api_key))
    #get_request(url, **kwargs)
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(NLU_URL, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey',API_KEY),
                                    params=params)
    except:
        # If any error occurs
        print("Network exception occurred")
    #Log response params        
    status_code = response.status_code
    print("With status {} ".format(status_code))
    print("Just the raw response {}".format(response))

    json_data = json.loads(response.text)
    print("the response {} ".format(json_data))
    print("NLU analysis {}".format(response))
    json_data = json_data["sentiment"]["document"]["label"]
    print("the result {} ".format(json_data))
    return json_data

text = "Great service"
json_resp = analyze_review_sentiments(text)