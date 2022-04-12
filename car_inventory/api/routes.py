from flask import Blueprint, jsonify, request
from flask_login import login_required
from car_inventory.helpers import token_required
from car_inventory.models import db,User,Car,car_schema,cars_schema

api = Blueprint('api',__name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({'some':'value',
                    'Other':44.3})

# Create Car Route
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    safety_quality = request.json['safety_quality']
    drive_time = request.json['drive_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    make = request.json['make']
    user_token = current_user_token.token

    car = Car(name, description,price,safety_quality,drive_time,max_speed,dimensions,
                weight,cost_of_production,make,user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve ALL cars
@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve a car
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token,id):
    owner = current_user_token.token
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# UPDATE a car
@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.name = request.json['name']
    car.description = request.json['description']
    car.price = request.json['price']
    car.safety_quality = request.json['safety_quality']
    car.drive_time = request.json['drive_time']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_production = request.json['cost_of_production']
    car.make = request.json['make']
    
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE a car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)