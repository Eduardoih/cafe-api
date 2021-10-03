from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)


##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=['GET'])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


## HTTP GET - Read Record

@app.route("/all", methods=['GET'])
def all_cafes_list():
    cafes_list = []
    cafes = db.session.query(Cafe).all()
    for cafe in cafes:
        each_cafe = {
            'id': cafe.id,
            'name': cafe.name,
            'location': cafe.location,
            'coffee_price': cafe.coffee_price,
            'seats': cafe.seats,
            'img_url': cafe.img_url,
            'map_url': cafe.map_url,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'has_toilet': cafe.has_toilet,
        }
        cafes_list.append(each_cafe)
    return jsonify(cafes_list)


@app.route("/search", methods=['GET'])
def search_cafe():
    location_selected = request.args.get('loc')
    query_location = Cafe.query.filter_by(location=location_selected).first()
    if query_location is None:
        return jsonify(error="Not Found: Sorry, we don't have a  cafe at that location.")
    return jsonify(cafe={
        "id": query_location.id,
        "name": query_location.name,
        "map_url": query_location.map_url,
        "img_url": query_location.img_url,
        "location": query_location.location,
        "seats": query_location.seats,
        "has_toilet": query_location.has_toilet,
        "has_wifi": query_location.has_wifi,
        "has_sockets": query_location.has_sockets,
        "can_take_calls": query_location.can_take_calls,
        "coffee_price": query_location.coffee_price,
    })

## HTTP POST - Create Record


@app.route("/add", methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response="success: Successfully added the new cafe.")


## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=['POST', 'GET'])
def update_cafe_price(cafe_id):
    price_to_update = request.args.get('new_price')
    cafe_to_update = Cafe.query.get(cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = price_to_update
        db.session.commit()
        return jsonify(response="success: Successfully updated the price."), 200
    return jsonify(error="Not Found: Sorry a cafe with that id was not found in the database."), 404


## HTTP DELETE - Delete Record


@app.route("/report-closed/<cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_inserted = request.args.get('api-key')
    if api_inserted == "TopSecretAPIKey":
        selected_cafe = Cafe.query.get(cafe_id)
        if selected_cafe:
            book_to_delete = Cafe.query.get(cafe_id)
            db.session.delete(book_to_delete)
            db.session.commit()
            return jsonify(response="success: Successfully deleted."), 200
        return jsonify(error="Not Found: Sorry a cafe with that id was not found in the database."), 404
    return jsonify(error="Sorry, that's not allowed. Make sure that the correct api_key."), 403


if __name__ == '__main__':
    app.run(debug=True)
