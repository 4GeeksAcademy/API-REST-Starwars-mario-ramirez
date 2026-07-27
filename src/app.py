"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    user_list = User.query.all()

    result = [user.serialize() for user in user_list]

    return jsonify(result), 200


@app.route('/people', methods=['GET'])
def get_people():

    people_list = People.query.all()

    results = [person.serialize() for person in people_list]

    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    person = People.query.get(people_id)

    if person:

        result = person.serialize()

        return jsonify(result), 200

    else: return jsonify("404 not found"), 404


@app.route('/planets', methods=['GET'])
def get_planets():
    planets_list = Planets.query.all()

    results = [planet.serialize() for planet in planets_list]

    return jsonify(results), 200


@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):
    planet = Planets.query.get(planets_id)

    if planet:
        result = planet.serialize()

        return jsonify(result), 200

    else: return jsonify("404 not found"), 404


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1

    new_favorite = Favorites(user_id=user_id, people_id=people_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Character added to favorites"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planets(planet_id):
    user_id = 1

    new_favorite = Favorites(user_id=user_id, planets_id=planet_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201


@app.route('/users/favorites', methods=['GET'])
def handdle_favorites():
    favorites = Favorites.query.filter_by(user_id=1).all()

    results = [favorite.serialize() for favorite in favorites]

    return jsonify(results), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorites_people(people_id):
    favorite_to_delete = Favorites.query.filter_by(user_id= 1, people_id=people_id).first()

    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()
        
        return jsonify({"msg":"Character deleted successfully"}), 200

    else: 
        return jsonify("404 not found"), 404


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorites_planets(planet_id):
    favorite_to_delete = Favorites.query.filter_by(user_id= 1, planets_id=planet_id).first()

    if favorite_to_delete:
        db.session.delete(favorite_to_delete)
        db.session.commit()

        return jsonify({"msg":"Planet deleted successfully"}), 200

    else:
        return jsonify("404 not found"), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)