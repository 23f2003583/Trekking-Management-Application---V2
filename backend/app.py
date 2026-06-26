from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Staff, Trek, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '3f98a21c5b8d4e7f9a1c2b3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f'
db.init_app(app)

jwt = JWTManager(app)

CORS(app)

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password']), role='user')
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200



@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful","data" :{"username": user.username, "email": user.email, "role": user.role, "access_token": access_token}}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    


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
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
