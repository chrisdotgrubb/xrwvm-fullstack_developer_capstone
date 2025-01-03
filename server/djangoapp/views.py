# Uncomment the required imports before adding the code

import json
import logging

from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments

# Get an instance of a logger
logger = logging.getLogger(__name__)

dealer_data = [
    {
      "id": 1,
      "city": "El Paso",
      "state": "Texas",
      "st": "TX",
      "address": "3 Nova Court",
      "zip": "88563",
      "lat": 31.6948,
      "long": -106.3,
      "short_name": "Holdlamis",
      "full_name": "Holdlamis Car Dealership"
    },
    {
      "id": 2,
      "city": "Minneapolis",
      "state": "Minnesota",
      "st": "MN",
      "address": "6337 Butternut Crossing",
      "zip": "55402",
      "lat": 44.9762,
      "long": -93.2759,
      "short_name": "Temp",
      "full_name": "Temp Car Dealership"
    },
    {
      "id": 3,
      "city": "Birmingham",
      "state": "Alabama",
      "st": "AL",
      "address": "9477 Twin Pines Center",
      "zip": "35285",
      "lat": 33.5446,
      "long": -86.9292,
      "short_name": "Sub-Ex",
      "full_name": "Sub-Ex Car Dealership"
    },
    {
      "id": 4,
      "city": "Dallas",
      "state": "Texas",
      "st": "TX",
      "address": "85800 Hazelcrest Circle",
      "zip": "75241",
      "lat": 32.6722,
      "long": -96.7774,
      "short_name": "Solarbreeze",
      "full_name": "Solarbreeze Car Dealership"
    },
    {
      "id": 5,
      "city": "Baltimore",
      "state": "Maryland",
      "st": "MD",
      "address": "93 Golf Course Pass",
      "zip": "21203",
      "lat": 39.2847,
      "long": -76.6205,
      "short_name": "Regrant",
      "full_name": "Regrant Car Dealership"
    },
    {
      "id": 6,
      "city": "Wilkes Barre",
      "state": "Pennsylvania",
      "st": "PA",
      "address": "2 Burrows Hill",
      "zip": "18763",
      "lat": 41.2722,
      "long": -75.8801,
      "short_name": "Stronghold",
      "full_name": "Stronghold Car Dealership"
    },
    {
      "id": 7,
      "city": "Pueblo",
      "state": "Colorado",
      "st": "CO",
      "address": "9 Cambridge Park",
      "zip": "81010",
      "lat": 38.1286,
      "long": -104.5523,
      "short_name": "Job",
      "full_name": "Job Car Dealership"
    },
    {
      "id": 8,
      "city": "Topeka",
      "state": "Kansas",
      "st": "KS",
      "address": "288 Larry Place",
      "zip": "66642",
      "lat": 39.0429,
      "long": -95.7697,
      "short_name": "Bytecard",
      "full_name": "Bytecard Car Dealership"
    },
    {
      "id": 9,
      "city": "Dallas",
      "state": "Texas",
      "st": "TX",
      "address": "253 Hanson Junction",
      "zip": "75216",
      "lat": 32.7086,
      "long": -96.7955,
      "short_name": "Job",
      "full_name": "Job Car Dealership"
    },
    {
      "id": 10,
      "city": "Washington",
      "state": "District of Columbia",
      "st": "DC",
      "address": "108 Memorial Pass",
      "zip": "20005",
      "lat": 38.9067,
      "long": -77.0312,
      "short_name": "Alphazap",
      "full_name": "Alphazap Car Dealership"
    },
    {
      "id": 11,
      "city": "Carol Stream",
      "state": "Illinois",
      "st": "IL",
      "address": "8108 Dryden Court",
      "zip": "60351",
      "lat": 41.9166,
      "long": -88.1208,
      "short_name": "Rank",
      "full_name": "Rank Car Dealership"
    },
    {
      "id": 12,
      "city": "Silver Spring",
      "state": "Maryland",
      "st": "MD",
      "address": "168 Pawling Lane",
      "zip": "20918",
      "lat": 39.144,
      "long": -77.2076,
      "short_name": "Tin",
      "full_name": "Tin Car Dealership"
    },
    {
      "id": 13,
      "city": "Baltimore",
      "state": "Maryland",
      "st": "MD",
      "address": "452 Fair Oaks Drive",
      "zip": "21275",
      "lat": 39.2847,
      "long": -76.6205,
      "short_name": "Y-Solowarm",
      "full_name": "Y-Solowarm Car Dealership"
    },
    {
      "id": 14,
      "city": "San Francisco",
      "state": "California",
      "st": "CA",
      "address": "2109 Scott Parkway",
      "zip": "94147",
      "lat": 37.7848,
      "long": -122.7278,
      "short_name": "It",
      "full_name": "It Car Dealership"
    },
    {
      "id": 15,
      "city": "San Antonio",
      "state": "Texas",
      "st": "TX",
      "address": "5057 Pankratz Hill",
      "zip": "78225",
      "lat": 29.3875,
      "long": -98.5245,
      "short_name": "Tempsoft",
      "full_name": "Tempsoft Car Dealership"
    },
    {
      "id": 16,
      "city": "El Paso",
      "state": "Texas",
      "st": "TX",
      "address": "0 Rieder Trail",
      "zip": "79994",
      "lat": 31.6948,
      "long": -106.3,
      "short_name": "Treeflex",
      "full_name": "Treeflex Car Dealership"
    },
    {
      "id": 17,
      "city": "San Jose",
      "state": "California",
      "st": "CA",
      "address": "7670 American Ash Drive",
      "zip": "95138",
      "lat": 37.2602,
      "long": -121.7709,
      "short_name": "Home Ing",
      "full_name": "Home Ing Car Dealership"
    },
    {
      "id": 18,
      "city": "Whittier",
      "state": "California",
      "st": "CA",
      "address": "4 Pearson Avenue",
      "zip": "90605",
      "lat": 33.9413,
      "long": -118.0356,
      "short_name": "Bitchip",
      "full_name": "Bitchip Car Dealership"
    },
    {
      "id": 19,
      "city": "Hialeah",
      "state": "Florida",
      "st": "FL",
      "address": "93 Monument Circle",
      "zip": "33013",
      "lat": 25.8594,
      "long": -80.2725,
      "short_name": "Otcom",
      "full_name": "Otcom Car Dealership"
    },
    {
      "id": 20,
      "city": "Detroit",
      "state": "Michigan",
      "st": "MI",
      "address": "4580 Waubesa Lane",
      "zip": "48224",
      "lat": 42.4098,
      "long": -82.9441,
      "short_name": "Subin",
      "full_name": "Subin Car Dealership"
    },
    {
      "id": 21,
      "city": "San Francisco",
      "state": "California",
      "st": "CA",
      "address": "046 Mockingbird Junction",
      "zip": "94154",
      "lat": 37.7848,
      "long": -122.7278,
      "short_name": "Andalax",
      "full_name": "Andalax Car Dealership"
    },
    {
      "id": 22,
      "city": "Fort Lauderdale",
      "state": "Florida",
      "st": "FL",
      "address": "45737 Butternut Lane",
      "zip": "33330",
      "lat": 26.0663,
      "long": -80.3339,
      "short_name": "Y-Solowarm",
      "full_name": "Y-Solowarm Car Dealership"
    },
    {
      "id": 23,
      "city": "Des Moines",
      "state": "Iowa",
      "st": "IA",
      "address": "21425 Bartelt Pass",
      "zip": "50936",
      "lat": 41.6727,
      "long": -93.5722,
      "short_name": "Bitchip",
      "full_name": "Bitchip Car Dealership"
    },
    {
      "id": 24,
      "city": "Utica",
      "state": "New York",
      "st": "NY",
      "address": "408 Delaware Circle",
      "zip": "13505",
      "lat": 43.0872,
      "long": -75.2603,
      "short_name": "Aerified",
      "full_name": "Aerified Car Dealership"
    },
    {
      "id": 25,
      "city": "Washington",
      "state": "District of Columbia",
      "st": "DC",
      "address": "6505 Melrose Junction",
      "zip": "20580",
      "lat": 38.8933,
      "long": -77.0146,
      "short_name": "Opela",
      "full_name": "Opela Car Dealership"
    },
    {
      "id": 26,
      "city": "Pittsburgh",
      "state": "Pennsylvania",
      "st": "PA",
      "address": "306 Jenna Parkway",
      "zip": "15279",
      "lat": 40.4344,
      "long": -80.0248,
      "short_name": "Flowdesk",
      "full_name": "Flowdesk Car Dealership"
    },
    {
      "id": 27,
      "city": "San Antonio",
      "state": "Texas",
      "st": "TX",
      "address": "95321 Superior Hill",
      "zip": "78245",
      "lat": 29.4189,
      "long": -98.6895,
      "short_name": "Namfix",
      "full_name": "Namfix Car Dealership"
    },
    {
      "id": 28,
      "city": "Hialeah",
      "state": "Florida",
      "st": "FL",
      "address": "5458 Maple Way",
      "zip": "33018",
      "lat": 25.9098,
      "long": -80.3889,
      "short_name": "Fixflex",
      "full_name": "Fixflex Car Dealership"
    },
    {
      "id": 29,
      "city": "San Francisco",
      "state": "California",
      "st": "CA",
      "address": "9 Harper Circle",
      "zip": "94110",
      "lat": 37.7509,
      "long": -122.4153,
      "short_name": "Fix San",
      "full_name": "Fix San Car Dealership"
    },
    {
      "id": 30,
      "city": "Houston",
      "state": "Texas",
      "st": "TX",
      "address": "5423 Spaight Road",
      "zip": "77218",
      "lat": 29.834,
      "long": -95.4342,
      "short_name": "Opela",
      "full_name": "Opela Car Dealership"
    },
    {
      "id": 31,
      "city": "New York City",
      "state": "New York",
      "st": "NY",
      "address": "5 Northfield Pass",
      "zip": "10131",
      "lat": 40.7808,
      "long": -73.9772,
      "short_name": "Fintone",
      "full_name": "Fintone Car Dealership"
    },
    {
      "id": 32,
      "city": "Wilkes Barre",
      "state": "Pennsylvania",
      "st": "PA",
      "address": "3 Carey Junction",
      "zip": "18768",
      "lat": 41.2722,
      "long": -75.8801,
      "short_name": "Subin",
      "full_name": "Subin Car Dealership"
    },
    {
      "id": 33,
      "city": "Des Moines",
      "state": "Iowa",
      "st": "IA",
      "address": "627 Cottonwood Circle",
      "zip": "50335",
      "lat": 41.6727,
      "long": -93.5722,
      "short_name": "Tres-Zap",
      "full_name": "Tres-Zap Car Dealership"
    },
    {
      "id": 34,
      "city": "Silver Spring",
      "state": "Maryland",
      "st": "MD",
      "address": "8 Green Hill",
      "zip": "20904",
      "lat": 39.0668,
      "long": -76.9969,
      "short_name": "Gembucket",
      "full_name": "Gembucket Car Dealership"
    },
    {
      "id": 35,
      "city": "Seattle",
      "state": "Washington",
      "st": "WA",
      "address": "9 Beilfuss Trail",
      "zip": "98158",
      "lat": 47.4497,
      "long": -122.3076,
      "short_name": "Treeflex",
      "full_name": "Treeflex Car Dealership"
    },
    {
      "id": 36,
      "city": "Vienna",
      "state": "Virginia",
      "st": "VA",
      "address": "311 Paget Alley",
      "zip": "22184",
      "lat": 38.8318,
      "long": -77.2888,
      "short_name": "Latlux",
      "full_name": "Latlux Car Dealership"
    },
    {
      "id": 37,
      "city": "Detroit",
      "state": "Michigan",
      "st": "MI",
      "address": "152 Moland Lane",
      "zip": "48224",
      "lat": 42.4098,
      "long": -82.9441,
      "short_name": "Ventosanzap",
      "full_name": "Ventosanzap Car Dealership"
    },
    {
      "id": 38,
      "city": "Dallas",
      "state": "Texas",
      "st": "TX",
      "address": "821 New Castle Trail",
      "zip": "75226",
      "lat": 32.7887,
      "long": -96.7676,
      "short_name": "Zamit",
      "full_name": "Zamit Car Dealership"
    },
    {
      "id": 39,
      "city": "Fresno",
      "state": "California",
      "st": "CA",
      "address": "990 Raven Road",
      "zip": "93740",
      "lat": 36.7464,
      "long": -119.6397,
      "short_name": "Stronghold",
      "full_name": "Stronghold Car Dealership"
    },
    {
      "id": 40,
      "city": "Merrifield",
      "state": "Virginia",
      "st": "VA",
      "address": "89375 Main Trail",
      "zip": "22119",
      "lat": 38.8318,
      "long": -77.2888,
      "short_name": "Greenlam",
      "full_name": "Greenlam Car Dealership"
    },
    {
      "id": 41,
      "city": "Baltimore",
      "state": "Maryland",
      "st": "MD",
      "address": "9 Sherman Hill",
      "zip": "21275",
      "lat": 39.2847,
      "long": -76.6205,
      "short_name": "Tres-Zap",
      "full_name": "Tres-Zap Car Dealership"
    },
    {
      "id": 42,
      "city": "Jersey City",
      "state": "New Jersey",
      "st": "NJ",
      "address": "62 Manley Point",
      "zip": "07310",
      "lat": 40.7324,
      "long": -74.0431,
      "short_name": "Konklab",
      "full_name": "Konklab Car Dealership"
    },
    {
      "id": 43,
      "city": "Atlanta",
      "state": "Georgia",
      "st": "GA",
      "address": "91 Declaration Avenue",
      "zip": "31119",
      "lat": 33.8913,
      "long": -84.0746,
      "short_name": "Opela",
      "full_name": "Opela Car Dealership"
    },
    {
      "id": 44,
      "city": "Roanoke",
      "state": "Virginia",
      "st": "VA",
      "address": "0 Northview Point",
      "zip": "24014",
      "lat": 37.2327,
      "long": -79.9463,
      "short_name": "Veribet",
      "full_name": "Veribet Car Dealership"
    },
    {
      "id": 45,
      "city": "Norfolk",
      "state": "Virginia",
      "st": "VA",
      "address": "283 Mockingbird Plaza",
      "zip": "23509",
      "lat": 36.8787,
      "long": -76.2604,
      "short_name": "Konklux",
      "full_name": "Konklux Car Dealership"
    },
    {
      "id": 46,
      "city": "New Orleans",
      "state": "Louisiana",
      "st": "LA",
      "address": "527 Hayes Junction",
      "zip": "70165",
      "lat": 30.033,
      "long": -89.8826,
      "short_name": "Regrant",
      "full_name": "Regrant Car Dealership"
    },
    {
      "id": 47,
      "city": "Stamford",
      "state": "Connecticut",
      "st": "CT",
      "address": "840 Pepper Wood Crossing",
      "zip": "06905",
      "lat": 41.0888,
      "long": -73.5435,
      "short_name": "Prodder",
      "full_name": "Prodder Car Dealership"
    },
    {
      "id": 48,
      "city": "Tucson",
      "state": "Arizona",
      "st": "AZ",
      "address": "48610 Morning Street",
      "zip": "85710",
      "lat": 32.2138,
      "long": -110.824,
      "short_name": "It",
      "full_name": "It Car Dealership"
    },
    {
      "id": 49,
      "city": "Athens",
      "state": "Georgia",
      "st": "GA",
      "address": "222 Grasskamp Plaza",
      "zip": "30605",
      "lat": 33.9321,
      "long": -83.3525,
      "short_name": "Veribet",
      "full_name": "Veribet Car Dealership"
    },
    {
      "id": 50,
      "city": "Atlanta",
      "state": "Georgia",
      "st": "GA",
      "address": "76 Clove Trail",
      "zip": "30316",
      "lat": 33.7217,
      "long": -84.3339,
      "short_name": "Aerified",
      "full_name": "Aerified Car Dealership"
    }
  ]
# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print(request)
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except: # noqa
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name, password=password,
                                        email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append(
            {"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    # return JsonResponse({"status": 200, "dealers": dealer_data})
    if (state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if (dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if (dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
def add_review(request):
    if request.user.is_anonymous is False:
        try:
            return JsonResponse({"status": 200})
        except: # noqa
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

# Module import
from .restapis import get_request, analyze_review_sentiments, post_review, searchcars_request

# Code for the view
def get_inventory(request, dealer_id):
    data = request.GET
    if (dealer_id):
        if 'year' in data:
            endpoint = "/carsbyyear/"+str(dealer_id)+"/"+data['year']
        elif 'make' in data:
            endpoint = "/carsbymake/"+str(dealer_id)+"/"+data['make']
        elif 'model' in data:
            endpoint = "/carsbymodel/"+str(dealer_id)+"/"+data['model']
        elif 'mileage' in data:
            endpoint = "/carsbymaxmileage/"+str(dealer_id)+"/"+data['mileage']
        elif 'price' in data:
            endpoint = "/carsbyprice/"+str(dealer_id)+"/"+data['price']
        else:
            endpoint = "/cars/"+str(dealer_id)
 
        cars = searchcars_request(endpoint)
        return JsonResponse({"status": 200, "cars": cars})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    return JsonResponse({"status": 400, "message": "Bad Request"})