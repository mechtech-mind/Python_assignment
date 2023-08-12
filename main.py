import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):


# ... (User model definition here) ...

db.create_all()

DUMMY_JSON_API = 'https://dummyjson.com/users/search?q=first_name'


@app.route('/api/users', methods=['GET'])
def get_users_by_first_name():
    first_name = request.args.get('first_name')
    if not first_name:
        return jsonify({'error': 'Missing mandatory query parameter: first_name'}), 400

    users = User.query.filter_by(first_name=first_name).all()
    if users:
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'gender': user.gender,
                'email': user.email,
                'phone': user.phone,
                'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None
            })
        return jsonify(user_list)
    else:
        response = requests.get(f'{DUMMY_JSON_API}?q={first_name}')
        dummy_users = response.json()

        for dummy_user in dummy_users:
            new_user = User(
                first_name=dummy_user['first_name'],
                last_name=dummy_user['last_name'],
                age=dummy_user['age'],
                gender=dummy_user['gender'],
                email=dummy_user['email'],
                phone=dummy_user['phone'],
                birth_date=dummy_user['birth_date']
            )
            db.session.add(new_user)
            db.session.commit()

        return jsonify(dummy_users)


if __name__ == '__main__':
    app.run(debug=True)
