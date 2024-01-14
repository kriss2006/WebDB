from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://1234:7890@db:3306/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        users = User.query.all()
        users_list = [{'id': user.id, 'name': user.name} for user in users]
        return jsonify(users_list)
    
    elif request.method == 'POST':
        data = request.json
        new_name = data.get('name')
        if new_name:
            new_user = User(name=new_name)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User added successfully'})

@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify({'id': user.id, 'name': user.name})

    elif request.method == 'PUT':
        new_name = request.json.get('name')
        if new_name:
            user.name = new_name
            db.session.commit()
            return jsonify({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
