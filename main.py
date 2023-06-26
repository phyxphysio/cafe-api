import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

#Create flask app
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////cafes.db'
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
    
@app.route('/random')
def random():
    import random 
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)

    return jsonify({
        'name': random_cafe.name,
        'map_url': random_cafe.map_url,
        'img_url': random_cafe.img_url,
        'location': random_cafe.location,
        'seats': random_cafe.seats,
        'has_toilet': random_cafe.has_toilet,
        'has_wifi': random_cafe.has_wifi,
        'has_sockets': random_cafe.has_sockets,
        'can_take_calls': random_cafe.can_take_calls,
        'coffee_price': random_cafe.coffee_price
    })

@app.route('/all')
def all():
    all_cafes = db.session.query(Cafe).all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_dict = {
        'name': cafe.name,
        'map_url': cafe.map_url,
        'img_url': cafe.img_url,
        'location': cafe.location,
        'seats': cafe.seats,
        'has_toilet': cafe.has_toilet,
        'has_wifi': cafe.has_wifi,
        'has_sockets': cafe.has_sockets,
        'can_take_calls': cafe.can_take_calls,
        'coffee_price': cafe.coffee_price
        }
        cafe_list.append(cafe_dict)

    return jsonify(cafe_list)

## HTTP GET - Read Record
@app.route('/search')
def search():
    loc = request.args.get("loc")

    cafes = Cafe.query.filter_by(location=loc).all()
    if cafes == []:
        return jsonify(error={'Error':'Cafe not found'})
    cafe_list = []
    for cafe in cafes:
        cafe_dict = {
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'has_sockets': cafe.has_sockets,
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price
            }
        cafe_list.append(cafe_dict)
    return jsonify(cafe_dict)

## HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add():
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
        coffee_price=request.form.get("coffee_price")

    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={'Success': 'Successfully added cafe.'})

## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:id>', methods=['PATCH'])
def update(id):
    cafe_id = id
    new_price = request.args.get('new_price')
    if cafe := Cafe.query.get(cafe_id):
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(success= {'Success': 'Updated price!'})
    else:
        return jsonify(error={'Error':'Cafe not found'}), 404
    

## HTTP DELETE - Delete Record
@app.route('/report-closed/<id>', methods={'DELETE'})
def delete(id):
    api_key = request.args.get('api-key')
    if api_key != 'TopSecretAPIKey':
        return jsonify(error= {'Not allowed': 'Make sure you have the right api-key'}), 403
    if cafe := Cafe.query.get(id):
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(success= {'Success': 'Deleted cafe!'})
    else :
        return jsonify(error={'Error':'Cafe not found'}), 404 

if __name__ == '__main__':
    app.run(port=5002)
