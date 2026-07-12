from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    role = db.Column(db.String(50), nullable=False, default='user') 
    status = db.Column(db.String(50), nullable=False, default='Active')
    treks = db.relationship('Trek', backref='staff_member', lazy=True)
    is_deleted = db.Column(db.Boolean, default=False) 

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    available_slots = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float, nullable=False)  
    status = db.Column(db.String(50), nullable=False, default='Open') 
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date )
    is_deleted = db.Column(db.Boolean, default=False)

    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)  
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending') 
    is_deleted = db.Column(db.Boolean, default=False)
