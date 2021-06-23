import random
import uuid
import boto3
import requests
from boto3.dynamodb.conditions import Key
from chalice import Chalice

app = Chalice(app_name='restaurant-journal')


@app.route('/')
def index():
    return {'hello': 'world'}


# Endpoint chooses a random restaurant from the parameters given,
# term = Type of food. eg.Chinese, Italian, American, etc
# location = City, State
@app.route('/random-restaurant/{term}/{location}/{api_key}', methods=['GET'], cors=True)
def random_restaurant(term, location, api_key):
    return restaurant_chooser(term, location, api_key)


@app.route('/create_review', methods=['POST'], cors=True)
def review_restaurant():
    # This is the JSON body the user sent in their POST request.
    review = app.current_request.json_body
    return dynamo_create_review(review)


# Endpoint that gets the user reviews
@app.route('/get_reviews', methods=['GET'], cors=True)
def get_restaurant_reviews():
    return dynamo_retrieve_reviews()

#PLANNER Endpoints
@app.route('/create_planner', methods=['POST'], cors=True)
def planner_restaurant():
    # This is the JSON body the user sent in their POST request.
    review = app.current_request.json_body
    return dynamo_create_planner(review)

# Endpoint that gets the user reviews
@app.route('/get_plans', methods=['GET'], cors=True)
def get_restaurant_planner():
    return dynamo_retrieve_planner()

# CONTROLLER METHODS


def restaurant_chooser(term, location, api_key):
    url = f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)

    # list of restaurants from Yelp API
    businesses_list = r.json().get("businesses")
    # size of the restaurant list
    list_size = len(businesses_list)
    # chooses a random number to recommend the restaurant
    restaurant_number = random.randint(0, list_size)

    name = businesses_list[restaurant_number].get("name")
    image_url = businesses_list[restaurant_number].get("image_url")
    is_closed = businesses_list[restaurant_number].get("is_closed")
    url = businesses_list[restaurant_number].get("url")
    categories = businesses_list[restaurant_number].get("categories")
    rating = businesses_list[restaurant_number].get("rating")
    price = businesses_list[restaurant_number].get("price")
    location = businesses_list[restaurant_number].get("location")

    business_dict = {
        "name": name,
        "image_url": image_url,
        "url": url,
        "categories": categories,
        "rating": rating,
        "price": price,
        "location": location,
    }

    return business_dict


# Creates the user review and stores it in Dynamodb reviews-logger
def dynamo_create_review(review):
    client = boto3.resource('dynamodb')
    table = client.Table('reviews-logger')
    user_id = "Andrew"  # TODO: Change later with login
    restaurant_name = review.get("restaurant_name")
    response = table.put_item(
        # Query that stores the review of the user. The query is always named Item
        Item={
            # Used uuid5 instead uuid4 to get rid of duplicates
            'id': str(uuid.uuid5(uuid.NAMESPACE_URL, f"{user_id}{restaurant_name}")),
            'user_id': user_id,
            'restaurant_name': restaurant_name,
            'title': review.get('title'),
            'rating': review.get('rating'),
            'review': review.get('review')
        }
    )
    item = response
    print(item)


# Retrieves the reviews of the user
def dynamo_retrieve_reviews():
    client = boto3.resource('dynamodb')
    table = client.Table('reviews-logger')
    # Displays all the reviews of the user
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq('Andrew') #TODO change the equal
    )

    return response.get("Items")  # response.get() to obtain only the list of reviews

# PLANNER methods
# Creates the planner
def dynamo_create_planner(planner):
    client = boto3.resource('dynamodb')
    table = client.Table('plans-logger')
    user_id = "Andrew"  # TODO change the user ID
    restaurant_name = planner.get("restaurant_name")
    response = table.put_item(
        Item={
            'id': str(uuid.uuid5(uuid.NAMESPACE_URL, f"{user_id} {restaurant_name}")),
            'user_id': user_id,
            'restaurant_name': restaurant_name,
            'plan': planner.get('plan'),
            'budget': planner.get('budget')
        }
    )
    print(response)

# Retrieves the planner
def dynamo_retrieve_planner():
    client = boto3.resource('dynamodb')
    table = client.Table('plans-logger')
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq('Andrew') #TODO change the equal
    )

    return response.get("Items")

