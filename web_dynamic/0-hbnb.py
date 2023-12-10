#!/usr/bin/python3
""" 0-hbnb.py solution"""
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
    """ start  """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    cache_id = uuid.uuid4()

    """Optimized sorting"""
    states = sorted(states, key=lambda k: k.name)
    cities = {}
    for state in states:
        state_cities = sorted(state.cities, key=lambda k: k.name)
        cities[state.id] = state_cities

    """ Lazy loading of places """
    places = {}
    def get_places(state_id):
        if state_id not in places:
            places[state_id] = storage.all(Place).filter(Place.state_id == state_id)
        return places[state_id]

    return render_template('0-hbnb.html',
                           states=states,
                           cities=cities,
                           amenities=amenities,
                           get_places=get_places,
                           cache_id=cache_id)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
