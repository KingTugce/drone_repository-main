# standard library imports
import uuid
from datetime import datetime
import secrets
# 3rd party imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
# adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# user model creation
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default = '')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email_name = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = "owner", lazy = True)



    def __init__(self, email, first_name = '', last_name = '', id='', password='', token='',g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email_name = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


    def __repr__(self):
        return f'User {self.email_name} has been added to the database.'


class Car(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    safety_quality = db.Column(db.String(50), nullable = True)
    drive_time = db.Column(db.String(100))
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    make = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, safety_quality, drive_time, max_speed, dimensions, 
                    weight, cost_of_production, make, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.safety_quality = safety_quality
        self.drive_time = drive_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_production = cost_of_production
        self.make = make
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following Car has been created: {self.name}"

        
# Creation of API Schema via the Marshmallow Object
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'safety_quality', 'drive_time', 'max_speed', 
                'dimensions', 'weight', 'cost_of_production', 'make']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)