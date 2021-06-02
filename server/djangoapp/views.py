from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            #return render(request, 'djangoapp/user_login.html', context)
            return redirect('djangoapp:index')
    else:
        #return render(request, 'djangoapp/user_login.html', context)
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = dict()
    row_cell = dict()
    row = dict()
    if request.method == "GET":
        url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #debug: print("delaer obj is type {}".format(dealerList))

    ## Map cardealer obj list to context dict
    # 
    # 

    i = 0    
    for dealer in dealerships:
        row_cell["address"] = dealer.address
        row_cell["city"] = dealer.city
        row_cell["full_name"] = dealer.full_name
        row_cell["id"] =dealer.id
        row_cell["st"] = dealer.st
        row_cell["state"] = dealer.state

        context[i] = row_cell
        row_cell = dict()
        i = i + 1

    print("****OCntext dict {}******".format(context))


    # Concat all dealer's short name
    #dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
    # Return a list of dealer short name

    #return HttpResponse(context[0]["address"])
    render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    print("Enter get_dealer_details")

    if request.method == "GET":
        url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/reviews/reviews?dealership="
        #append id to api url
        url = url +  str(dealer_id)
        print("Query review with URL {}".format(url))
        # Get reviews by dealers id from the URL
        reviews = get_dealer_by_id_from_cf(url, dealer_id)
        # Concat all dealer's short name
        review_text = ' '.join([rev.sentiment for rev in reviews])
        # Return a list of dealer short name
        print("exit get_dealer_details")
        return HttpResponse(review_text)
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    print("***Start add_review****")
    #Check wheter user is Logged in 
    if request.user.is_authenticated:
        print("********Logged in*********")
        review = dict()
        review["name"] = "James Headfield"
        review["dealership"] = dealer_id
        review["review"] = "I love their service desk"
        review["purchase"] = True
        review["car_model"] = "Volkswagen"

        json_payload = review
        #json_payload["review"] = review

        #print("JSON Payload {}".format(json_payload))

        url = "https://32dc2b02.eu-gb.apigw.appdomain.cloud/api/reviews/new"
        response = post_request(url, json_payload, dealerId=dealer_id)

        status_resp = response.status_code
        print("POST response status {}".format(status_resp))

        #Get reponse content
        post_response = response.text
        print("POST response text {}".format(post_response))

        return HttpResponse(post_response)
    else:
        # If not, return to login page again
        #return render(request, 'djangoapp/user_login.html', context)
        print("Not logged in")
        #return redirect('djangoapp:index')        
        return HttpResponse("User not authenticated") 
    # Handles POST request



