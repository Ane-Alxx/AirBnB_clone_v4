#!/usr/bin/python3
"""4-hbnb.py solution"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template, request
import uuid

app = Flask(__name__)

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/0-hbnb/', strict_slashes=False)
def hbnb():

    """ Optimize sorting"""
    states = sorted(storage.all(State).values(), key=lambda k: k.name)

    """ Create and use dictionaries for cities and places"""
    cities = {}
    places = {}
    def get_cities(state_id):
        if state_id not in cities:
            cities[state_id] = sorted(storage.all(City).filter(City.state_id == state_id), key=lambda k: k.name)
        return cities[state_id]

    def get_places(state_id):
        if state_id not in places:
            places[state_id] = storage.all(Place).filter(Place.state_id == state_id)
        return places[state_id]

    """Optimize data transfer and lazy loading"""
    amenities = sorted(storage.all(Amenity).values(), key=lambda k: k.name)

    cache_id = uuid.uuid4()

    return render_template('0-hbnb.html',
                           states=states,
                           get_cities=get_cities,
                           get_places=get_places,
                           amenities=amenities,
                           cache_id=cache_id)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
