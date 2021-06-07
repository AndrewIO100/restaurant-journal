import random

import requests


def foo():
    url = "https://api.yelp.com/v3/businesses/search?term=Chinese takeout&location=Ames, Iowa"
    headers = {"Authorization": "Bearer dP7ema0d4sMqlW7K-nbZkjwLGrRwGp-26M-FyEtVzacEqFV8Pn3VG_VuhL-NZUshSRT0ZtJhLvlixb53M_fCZ8-xztkAmmbwS1YpOSgKqaGn2xOONrpk02KRQhG4YHYx"}
    r = requests.get(url, headers=headers)

    # list of restaurants from Yelp API
    businesses_list = r.json().get("businesses")
    # size of the restaurant list
    list_size = len(businesses_list)
    # chooses a random number to recommend the restaurant
    restaurant_number = random.randint(0 , list_size)

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
        "categories":categories,
        "rating": rating,
        "price": price,
        "location": location,
    }

    return business_dict

