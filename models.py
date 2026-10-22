from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    role = db.Column(db.String, nullable=False, default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    dish = db.relationship('Dish', back_populates='orders')


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    slug = db.Column(db.String, nullable=False, unique=True)

    dishes = db.relationship('Dish', back_populates='category', order_by='Dish.name')

    def __repr__(self):
        return f"<Category {self.name}>"

class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    price = db.Column(db.Integer, nullable=False)#write emoji def
    emoji = db.Column(db.String, nullable=False, default='')
    is_avaliable = db.Column(db.Boolean, nullable=False, default=True)



    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='dishes')

    orders = db.relationship('Order', back_populates='dish', order_by='Order.id')

    def __repr__(self):
        return f"<Dish {self.name} {self.price} грн>"