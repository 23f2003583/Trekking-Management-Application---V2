from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Trek , Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
from flask_caching import Cache 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '3f98a21c5b8d4e7f9a1c2b3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f'
app.config['CACHE_TYPE'] ='RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
db.init_app(app)

jwt = JWTManager(app)
cache = Cache(app)
CORS(app)

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Username and/or email already exists'}), 400

    user = User(username=data['username'],
                email=data['email'],
                password=generate_password_hash(data['password']),
                name=data['name']
                )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role}
    )
    # return jsonify({"message": "User registered successfully"}), 200
    treks = Trek.query.all()
    trek_data = []
    for trek in treks:
        trek_data.append({
            'id': trek.id,
            'name': trek.name,
            'description': trek.description,
            'difficulty': trek.difficulty,
            'duration': trek.duration,
            'location': trek.location,
            'available_slots': trek.available_slots,
            'start_date': trek.start_date,
            'end_date': trek.end_date,
            'staff_id': trek.staff_id,
            'price': trek.price,
            'status': trek.status,
            'is_deleted': trek.is_deleted
        })
    return jsonify({
        "message": "User registered successfully", 
        "access_token": access_token, 
        "data": trek_data
    }), 200


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'],role='user').first()
    if user.is_deleted and check_password_hash(user.password, data['password']):
        return jsonify({"message": "User account is Deleted"}), 403
    elif user.status == 'Inactive'  and check_password_hash(user.password, data['password']):
        return jsonify({"message": "User account is inactive "}), 403
    elif user.status == 'Blacklist' and check_password_hash(user.password, data['password']):
        return jsonify({"message": "User account is blacklisted"}), 403
    elif user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role}
        )
        return jsonify({"message": "Login successful","data" :{"username": user.username, "email": user.email, "role": user.role, "access_token": access_token}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = User.query.filter_by(username=data['username'], role='admin').first()
    if admin and check_password_hash(admin.password, data['password']):
        access_token = create_access_token(
            identity=str(admin.id), 
            additional_claims={"role": admin.role}
        )
        return jsonify({"message": "Admin login successful","data" :{"username": admin.username, "email": admin.email, "role": admin.role, "access_token": access_token}}), 200
    else:
        return jsonify({"message": "Invalid admin username or password"}), 401

@app.route('/api/staff/login', methods=['POST'])
def staff_login():
    data = request.get_json()
    staff = User.query.filter_by(username=data['username'], role='staff').first()

    if staff and check_password_hash(staff.password, data['password']):
        access_token = create_access_token(
            identity=str(staff.id),
            additional_claims={"role": staff.role}
        )
        return jsonify({"message": "Staff login successful","data" :{"id": staff.id, "username": staff.username, "email": staff.email, "role": staff.role, "access_token": access_token}}), 200
    else:
        return jsonify({"message": "Invalid staff username or password"}), 401

@app.route('/api/admin_home', methods=['GET'])
@jwt_required()
def admin_home():
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    trek_count = Trek.query.filter_by(is_deleted=False).count()
    user_count = User.query.filter_by(role='user', is_deleted=False).count()
    staff_count = User.query.filter_by(role='staff', is_deleted=False).count()
    booking_count = Booking.query.filter_by(is_deleted=False).count()

    return jsonify({
        "trek_count": trek_count,
        "user_count": user_count,
        "staff_count": staff_count,
        "booking_count": booking_count
    }), 200













#-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
#-/-/-/-/-/-/-/-/-/-/-/-/-/-/-ADMIN-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/



#-/-/-/-/-/-/-/-/-/-/-/-/-/-/-TREKS-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

@app.route('/api//create_trek', methods=['POST'])
@jwt_required()
def create_trek():
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    trek = Trek(
        name=data['name'],
        description=data['description'],
        difficulty=data['difficulty'],
        duration=data['duration'],
        location=data['location'],
        available_slots=data['available_slots'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else datetime.strptime('2023-01-01', '%Y-%m-%d').date(),
        staff_id=data['staff_id'],
        price=data.get('price', 0.00)
        )
    db.session.add(trek)
    db.session.commit()

    return jsonify({"message": "Trek created successfully"}), 200

@app.route('/api/get_treks', methods=['GET'])
@jwt_required(optional=True)
@cache.cached(timeout=60)
def get_treks():
    # if get_jwt().get('role') != 'admin':
    #     return jsonify({"message": "Unauthorized"}), 401
    current_user_id = get_jwt_identity()
    treks = Trek.query.all()
    data=[]
    for trek in treks:
        staff_member = User.query.get(trek.staff_id)
        staff_name = staff_member.name if staff_member else None
        user_booking_status = None
        user_booking_id =None
        if current_user_id:
            booking = Booking.query.filter_by(user_id=current_user_id, trek_id=trek.id).first()
            if booking:
                user_booking_status = booking.status
                user_booking_id =booking.id

        trek_data = {
            'id': trek.id,
            'name': trek.name,
            'description': trek.description,
            'difficulty': trek.difficulty,
            'duration': trek.duration,
            'location': trek.location,
            'available_slots': trek.available_slots,
            'start_date': trek.start_date.strftime('%d-%m-%Y') if trek.start_date else None,
            'end_date': trek.end_date.strftime('%d-%m-%Y') if trek.end_date else None,
            'staff_id': trek.staff_id,
            'price': trek.price,
            'status': trek.status,
            'is_deleted': trek.is_deleted,
            'staff_name': staff_name,
            'my_booking_status': user_booking_status,
            'my_booking_id': user_booking_id 
        }
        data.append(trek_data)
    data.sort(key=lambda x: x['is_deleted'])
    return jsonify(data), 200



@app.route('/api/bookings/<int:trek_id>', methods=['GET'])
# @jwt_required()
def get_bookings_of_trek(trek_id):
    if get_jwt().get('role') != 'User':
        return jsonify({"message": "Unauthorized"}), 401

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    data = []
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        user = User.query.get(booking.user_id)
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'user_name': user.name if user else None,
            'trek_id': booking.trek_id,
            'trek_name': trek.name if trek else None,
            'booking_date': booking.booking_date,
            'status': booking.status
        }
        data.append(booking_data)
    return jsonify(data), 200


@app.route('/api/get_trek/<int:trek_id>', methods=['GET'])
@jwt_required()
def get_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    return jsonify(trek.to_dict()), 200


@app.route('/api/update_trek/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    if get_jwt().get('role') == 'user':
        return jsonify({"message": "Unauthorized"}), 401

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()
    
    trek.name = data.get('name', trek.name)
    trek.description = data.get('description', trek.description)
    trek.difficulty = data.get('difficulty', trek.difficulty)
    trek.duration = data.get('duration', trek.duration)
    trek.location = data.get('location', trek.location)
    trek.available_slots = data.get('available_slots', trek.available_slots)
    trek.staff_id = data.get('staff_id', trek.staff_id)
    trek.price = data.get('price', trek.price) 
    
    start_date_str = data.get('start_date')
    if start_date_str:
        trek.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()


    end_date_str = data.get('end_date')
    if end_date_str:
        trek.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    cache.clear()

    db.session.commit()

    return jsonify({"message": "Trek updated successfully"}), 200

@app.route('/api/delete_trek/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    trek = Trek.query.get(trek_id)
    if not trek or trek.is_deleted:
        return jsonify({"message": "Trek not found"}), 404

    trek.is_deleted = True
    trek.status = 'Inactive' 
    cache.clear()

    db.session.commit()

    return jsonify({"message": "Trek deleted successfully"}), 200

@app.route('/api/update_treks/<int:trek_id>/status', methods=['PUT'])
@jwt_required()
def update_trek_status(trek_id):
    if get_jwt().get('role') == 'user':
        return jsonify({"message": "Unauthorized"}), 401

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    if trek.status == 'Upcomming':
        trek.status = 'Open'
    elif trek.status == 'Open':
        trek.status = 'Closed'
    else:
        trek.status = 'Upcomming'
    cache.clear()
    db.session.commit()

    return jsonify({"message": "Trek status updated successfully"}), 200

# #-/-/-/-/-/-/-/-/-/-/-/-/-/-/-STAFFS-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
@app.route('/api/create_staff', methods=['POST'])
@jwt_required()
def create_staff():
    try:
        if get_jwt().get('role') != 'admin':
            return jsonify({"message": "Unauthorized"}), 401

        data = request.get_json()
        if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Username or email already exists'}), 400
        
        staff = User(name=data['name'],
                    username=data['username'],
                    email=data['email'],
                    password=generate_password_hash(data['password']),
                    role='staff'
                    )
        
        selected_trek_ids = data.get('treks', [])
        
        for trek_id in selected_trek_ids:
            trek = Trek.query.get(trek_id)
            if trek:
                staff.treks.append(trek) 
                
        db.session.add(staff)
        db.session.commit()
        return jsonify({"message": "Staff created successfully"}), 200
    
    except Exception:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Internal Server Error"}), 500


@app.route('/api/get_staffs', methods=['GET'])
@jwt_required()
def get_staffs():
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    staff_members = User.query.filter_by(role='staff').all()
    data = []
    for staff in staff_members:
        
        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'username': staff.username,
            'email': staff.email,
            'role': staff.role,
            'status': staff.status,
            'is_deleted': staff.is_deleted,
            'treks': [{'id': trek.id, 'name': trek.name} for trek in staff.treks]
            

        }
        data.append(staff_data)
    data.sort(key=lambda x: x['is_deleted'])

    return jsonify(data), 200

@app.route('/api/get_treks_of_staff', methods=['GET'])
@jwt_required()
def get_treks_of_staff():
    if get_jwt().get('role') != 'staff':
        return jsonify({"message": "Unauthorized"}), 401
    staff_id =get_jwt_identity()
    treks = Trek.query.filter_by(staff_id=staff_id).all()
    data = []
    for trek in treks:
        staff_member = User.query.get(trek.staff_id)
        staff_name = staff_member.name if staff_member else None
        trek_data = {
            'id': trek.id,
            'name': trek.name,
            'description': trek.description,
            'difficulty': trek.difficulty,
            'duration': trek.duration,
            'location': trek.location,
            'available_slots': trek.available_slots,
            'start_date': trek.start_date,
            'end_date': trek.end_date,
            'staff_id': trek.staff_id,
            'price': trek.price,
            'status': trek.status,
            'is_deleted': trek.is_deleted,
            'staff_name': staff_name
        }
        data.append(trek_data)
    return jsonify(data), 200



@app.route('/api/staff/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    current_staff_id = get_jwt_identity()
    
    staff = User.query.get(current_staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    staff_data = {
        'id': staff.id,
        'name': staff.name,
        'username': staff.username,
        'email': staff.email,
        'role': staff.role,
        'status': staff.status,
        'is_deleted': staff.is_deleted,
        'treks': [{'id': trek.id, 'name': trek.name} for trek in staff.treks]
    }

    return jsonify(staff_data), 200

@app.route('/api/update_staff/<int:staff_id>', methods=['PUT'])
@jwt_required()
def update_staff(staff_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    staff = User.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    data = request.get_json()
    staff.username = data.get('username', staff.username)
    staff.name = data.get('name', staff.name)
    staff.email = data.get('email', staff.email)
    staff.treks = []
    selected_trek_ids = data.get('treks', [])
    for trek_id in selected_trek_ids:
        trek = Trek.query.get(trek_id)
        if trek:
            staff.treks.append(trek)
    db.session.commit()

    return jsonify({"message": "Staff updated successfully"}), 200


# #-/-/-/-/-/-/-/-/-/-/-/-/-/-/-USERS-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

@app.route('/api/get_users', methods=['GET'])
@jwt_required()
def get_users():
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    users = User.query.filter_by(role='user').all()

    data = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status,
            'is_deleted': user.is_deleted
        }
        data.append(user_data)
    data.sort(key=lambda x: x['is_deleted'])


    return jsonify(data), 200

@app.route('/api/get_bookings_of_user', methods=['GET'])
@jwt_required()
def get_bookings_of_user():
    if get_jwt().get('role') == 'staff':
        return jsonify({"message": "Unauthorized"}), 401
        
    current_user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=current_user_id).all()
    data = []
    
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        staff= User.query.get(trek.staff_id)
        
        if trek:
            trek_data = {
                'id': trek.id,
                'name': trek.name,
                'description': trek.description,
                'difficulty': trek.difficulty,
                'duration': trek.duration,
                'location': trek.location,
                'available_slots': trek.available_slots,
                'start_date': trek.start_date,
                'end_date': trek.end_date,
                'staff_id': trek.staff_id,
                'price': trek.price,
                'status': trek.status,
                'is_deleted': trek.is_deleted,     
                'booking_id': booking.id,          
                'booking_status': booking.status,
                'booking_date':booking.booking_date,
                'staff_name': staff.name if staff else "Unassigned"
            }
            data.append(trek_data)

    return jsonify(data), 200

@app.route('/api/get_bookings_of_staff', methods=['GET'])
@jwt_required()
def get_bookings_of_staff():
    if get_jwt().get('role') != 'staff':
        return jsonify({"message": "Unauthorized"}), 401
        
    current_user_id = get_jwt_identity()

    bookings = Booking.query.join(Trek).filter(Trek.staff_id == current_user_id).all()
    data = []
    
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        user = User.query.get(booking.user_id)
        
        if trek:
            trek_data = {
                'id': trek.id,
                'name': trek.name,
                'description': trek.description,
                'difficulty': trek.difficulty,
                'duration': trek.duration,
                'location': trek.location,
                'available_slots': trek.available_slots,
                'start_date': trek.start_date,
                'end_date': trek.end_date,
                'staff_id': trek.staff_id,
                'price': trek.price,
                'status': trek.status,
                'is_deleted': trek.is_deleted,     
                'booking_id': booking.id,          
                'booking_status': booking.status,
                'booking_date': booking.booking_date,
                'user_name': user.name if user else None,
                'username': user.username if user else None, 
                'email': user.email if user else None
            }
            data.append(trek_data)

    return jsonify(data), 200

@app.route('/api/get_users_of_staff', methods=['GET'])
@jwt_required()
def get_users_of_staff():
    if get_jwt().get('role') != 'staff':
        return jsonify({"message": "Unauthorized"}), 401
        
    current_staff_id = get_jwt_identity()

    bookings = Booking.query.join(Trek).filter(Trek.staff_id == current_staff_id).all()
    
    users_data = {}
    
    for booking in bookings:
        user = User.query.get(booking.user_id)
        trek = Trek.query.get(booking.trek_id)
        
        if user and trek:
            if user.id not in users_data:
                users_data[user.id] = {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'status': user.status,
                    'booked_treks': [] 
                }
            
            if trek.name not in users_data[user.id]['booked_treks']:
                users_data[user.id]['booked_treks'].append(trek.name)

    data = list(users_data.values())

    return jsonify(data), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.to_dict()), 200

@app.route('/api/delete_users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user or user.is_deleted:
        return jsonify({"message": "User not found"}), 404

    user.is_deleted = True
    user.status = 'Inactive'
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/api/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
def update_user_status(user_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.status == 'Active':
        user.status = 'Inactive'
    elif user.status == 'Inactive':
        user.status = 'Blacklist'
    else:
        user.status = 'Active'
    db.session.commit()

    return jsonify({"message": "User status updated successfully"}), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if get_jwt().get('role') != 'user':
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200





#BOOKINGS
@app.route('/api/book_trek/<int:trek_id>', methods=['POST'])
@jwt_required()
def book_trek(trek_id):
    if get_jwt().get('role') != 'user':
        return jsonify({"message": "Unauthorized"}), 401

    current_user_id = get_jwt_identity()

    trek = Trek.query.get(trek_id)
    booking = Booking.query.filter_by(user_id=current_user_id, trek_id=trek_id).first()
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    existing_booking = Booking.query.filter_by(user_id=current_user_id, trek_id=trek_id).first()
    if existing_booking:
        return jsonify({"message": "You have already booked this trek"}), 400
    
    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400
    
    if trek.status != 'Open':
        return jsonify({"message": "This trek is not open for booking"}), 400

    booking = Booking(user_id=current_user_id, trek_id=trek_id, booking_date=datetime.utcnow(), status='Pending')
    
    trek.available_slots -= 1
    
    db.session.add(trek)
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Trek booked successfully"}), 200

@app.route('/api/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    if get_jwt().get('role') != 'admin':
        return jsonify({"message": "Unauthorized"}), 401

    bookings = Booking.query.all()
    data = []
    
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        user = User.query.get(booking.user_id)
        if trek:
            staff = User.query.get(trek.staff_id) 
            
            trek_data = {
                'booking_id': booking.id,          
                'name': trek.name,
                'location': trek.location,
                'booking_date': booking.booking_date,
                'duration': trek.duration,
                
                'user_name': user.name if user else None,
                'email': user.email if user else None, 
                
                'staff_name': staff.name if staff else "Unassigned",
                'staff_email': staff.email if staff else "N/A",
                
                'start_date': trek.start_date,
                'end_date': trek.end_date,
                'status': trek.status,
                'booking_status': booking.status,
            }
            data.append(trek_data)

    return jsonify(data), 200



@app.route('/api/update_booking_status/<int:booking_id>/status', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    if get_jwt().get('role') == 'user':
        return jsonify({"message": "Unauthorized"}), 401

    booking = Booking.query.get(booking_id)
    trek = Trek.query.get(booking.trek_id) if booking else None
    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.status == 'Pending':
        booking.status = 'Confirmed'
    elif booking.status == 'Confirmed':
        trek.available_slots += 1
        db.session.add(trek)
        booking.status = 'Cancelled'
    elif booking.status == 'Cancelled':
        booking.status = 'Completed'

    else:
        booking.status = 'Pending'
        db.session.add(booking)
    db.session.commit()


    return jsonify({"message": "Booking status updated successfully"}), 200

@app.route('/api/cancel_bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    if get_jwt().get('role') != 'user':
        return jsonify({"message": "Unauthorized"}), 401

    booking = Booking.query.get(booking_id)
    trek = Trek.query.get(booking.trek_id) if booking else None
    
    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    db.session.delete(booking)
    if trek:
        trek.available_slots += 1
        db.session.add(trek)
    db.session.commit()

    return jsonify({"message": "Booking cancelled successfully"}), 200


@app.route('/api/user/summary', methods=['GET'])
@jwt_required()
def user_summary():
    user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    trek_summary = {}
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        if not trek:
            continue
            
        if trek.name not in trek_summary:
            trek_summary[trek.name] = {
                'total_bookings': 0,
                'total_cost': 0.0
            }
            
        trek_summary[trek.name]['total_bookings'] += 1
        trek_summary[trek.name]['total_cost'] += trek.price
        
    trek_names = []
    trek_counts = []
    trek_costs = []
    
    for trek_name, summary in trek_summary.items():
        trek_names.append(trek_name)  
        trek_counts.append(summary['total_bookings'])
        trek_costs.append(summary['total_cost'])
    
    total_spent = sum(summary['total_cost'] for summary in trek_summary.values())
    
    active_bookings = sum(1 for booking in bookings if booking.status == 'Confirmed')        
    completed_bookings = sum(1 for booking in bookings if booking.status == 'Completed')
    
    return jsonify({
        'trek_names': trek_names,
        'trek_counts': trek_counts,
        'trek_costs': trek_costs,
        'total_spent': total_spent,        
        'active_bookings': active_bookings,        
        'completed_bookings': completed_bookings,
        'total': len(bookings)
    }), 200

@app.route('/api/export/bookings', methods=['GET'])
@jwt_required()
def export_bookings():
    user_id = get_jwt_identity()
    
    from tasks import export_bookings_report
    
    export_bookings_report.delay(user_id)
    
    return jsonify({'message': 'Bookings report is being generated and will be sent to your email shortly.'}), 200



@app.route('/api/admin/summary', methods=['GET'])
@jwt_required()
def admin_summary():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    bookings = Booking.query.all()
    trek_summary = {}
    
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        if not trek:
            continue
            
        if trek.name not in trek_summary:
            trek_summary[trek.name] = {
                'total_bookings': 0,
                'total_revenue': 0.0
            }
            
        trek_summary[trek.name]['total_bookings'] += 1
        trek_summary[trek.name]['total_revenue'] += trek.price
        
    trek_names = []
    trek_counts = []
    trek_revenues = []
    
    for trek_name, summary in trek_summary.items():
        trek_names.append(trek_name)  
        trek_counts.append(summary['total_bookings'])
        trek_revenues.append(summary['total_revenue'])
    
    total_revenue = sum(summary['total_revenue'] for summary in trek_summary.values())

    staff_summary = {}
    all_treks = Trek.query.all()
    
    for trek in all_treks:
        if trek.staff_id: 
            staff = User.query.get(trek.staff_id)
            staff_name = staff.name if staff else f"Unknown (ID: {trek.staff_id})"
            
            if staff_name not in staff_summary:
                staff_summary[staff_name] = 0
            staff_summary[staff_name] += 1
            
    staff_names = list(staff_summary.keys())
    staff_trek_counts = list(staff_summary.values())
    
    return jsonify({
        'trek_names': trek_names,
        'trek_counts': trek_counts,
        'trek_revenues': trek_revenues,
        'total_revenue': total_revenue,        
        'total_bookings': len(bookings),
        'staff_names': staff_names,
        'staff_trek_counts': staff_trek_counts
    }), 200


@app.route('/api/staff/summary', methods=['GET'])
@jwt_required()
def staff_summary():
    if get_jwt().get('role') != 'staff':
        return jsonify({'message': 'Staff access required'}), 403

    staff_id = get_jwt_identity()
    
    staff_treks = Trek.query.filter_by(staff_id=staff_id).all()
    trek_ids = [trek.id for trek in staff_treks]
    
    bookings = Booking.query.filter(Booking.trek_id.in_(trek_ids)).all()
    
    trek_summary = {}
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        if not trek:
            continue
            
        if trek.name not in trek_summary:
            trek_summary[trek.name] = {
                'total_bookings': 0,
                'total_revenue': 0.0
            }
            
        trek_summary[trek.name]['total_bookings'] += 1
        trek_summary[trek.name]['total_revenue'] += trek.price
        
    trek_names = []
    trek_counts = []
    trek_revenues = []
    
    for trek_name, summary in trek_summary.items():
        trek_names.append(trek_name)  
        trek_counts.append(summary['total_bookings'])
        trek_revenues.append(summary['total_revenue'])
    
    total_revenue = sum(summary['total_revenue'] for summary in trek_summary.values())
    
    active_bookings = sum(1 for booking in bookings if booking.status == 'Confirmed')        
    completed_bookings = sum(1 for booking in bookings if booking.status == 'Completed')
    
    return jsonify({
        'trek_names': trek_names,
        'trek_counts': trek_counts,
        'trek_revenues': trek_revenues,
        'total_revenue': total_revenue,  
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,      
        'total_bookings': len(bookings)
    }), 200

@app.route('/api/admin/search', methods=['GET'])
@jwt_required()
def admin_search():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'treks': [], 'staff': [], 'users': []}), 200

    search_term = f"%{query}%"

    treks = Trek.query.filter(Trek.name.ilike(search_term), Trek.is_deleted != True).all()
    trek_data = [{'id': t.id, 'name': t.name, 'location': t.location} for t in treks]

    staff_members = User.query.filter(User.name.ilike(search_term), User.role == 'staff').all()
    staff_data = [{'id': s.id, 'name': s.name, 'email': s.email} for s in staff_members]

    users = User.query.filter(User.name.ilike(search_term), User.role == 'user').all()
    user_data = [{'id': u.id, 'name': u.name, 'email': u.email} for u in users]

    return jsonify({
        'treks': trek_data,
        'staff': staff_data,
        'users': user_data
    }), 200

@app.route('/api/user/search_treks', methods=['GET'])
@jwt_required()
def user_search_treks():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify([]), 200

    search_term = f"%{query}%"

    treks = Trek.query.filter(Trek.name.ilike(search_term), Trek.is_deleted != True).all()
    
    trek_data = [{
        'id': t.id,
        'name': t.name,
        'location': t.location,
        'start_date': t.start_date,
        'end_date': t.end_date,
        'status': t.status
    } for t in treks]

    return jsonify(trek_data), 200

@app.route('/', methods=['GET'])
def get_data():

    data = {
        'message': 'Hello, World!',
        'status': 'success'
    }
    return jsonify(data), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', name='Admin User', email='admin@gmail.com', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
