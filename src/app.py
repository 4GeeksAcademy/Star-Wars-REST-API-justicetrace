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
from models import db, User, Planet, Character, Favorite

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
def list_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))


    return jsonify(all_users), 200

@app.route('/people', methods=['GET'])
def list_people():
    people = Character.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person is None:
        raise APIException("person not found", status_code=404)
    return jsonify(person.serialized()), 200

# [GET] /people/<int:people_id> Get one single person's information.
# [GET] /planets Get a list of all the planets in the database.
# [GET] /planets/<int:planet_id> Get one single planet's information.
# Additionally, create the following endpoints to allow your StarWars blog to have users and favorites:

# [GET] /users/favorites Get all the favorites that belong to the current user.
# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
# [POST] /favorite/people/<int:people_id> Add new favorite people to the current user with the people id = people_id.
# [DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id.
# [DELETE] /favorite/people/<int:people_id> Delete a favorite people with the id = people_id.






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

