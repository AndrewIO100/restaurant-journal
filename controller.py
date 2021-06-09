import random
import uuid

import boto3
import requests
from boto3.dynamodb.conditions import Key

API_KEY = "dP7ema0d4sMqlW7K-nbZkjwLGrRwGp-26M-FyEtVzacEqFV8Pn3VG_VuhL-NZUshSRT0ZtJhLvlixb53M_fCZ8-xztkAmmbwS1YpOSgKqaGn2xOONrpk02KRQhG4YHYx"


def restaurant_chooser(term, location):
    url = f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
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
        # Query that stores the review of the user
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
        KeyConditionExpression=Key('user_id').eq('Andrew')
    )

    return response.get("Items") #response.get() to obtain only the list of reviews
