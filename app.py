from chalice import Chalice

from controller import restaurant_chooser, dynamo_create_review, dynamo_retrieve_reviews

app = Chalice(app_name='restaurant-journal')


@app.route('/')
def index():
    return {'hello': 'world'}


# Endpoint chooses a random restaurant from the parameters given,
# term = Type of food. eg.Chinese, Italian, American, etc
# location = City, State
@app.route('/random-restaurant/{term}/{location}')
def random_restaurant(term, location):
    return restaurant_chooser(term, location)


@app.route('/create_review', methods=['POST'])
def review_restaurant():
    # This is the JSON body the user sent in their POST request.
    review = app.current_request.json_body
    return dynamo_create_review(review)


# Endpoint that gets the user reviews
@app.route('/get_reviews', methods=['GET'])
def get_restaurant_reviews():
    return dynamo_retrieve_reviews()

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
