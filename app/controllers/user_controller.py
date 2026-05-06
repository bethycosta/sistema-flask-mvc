from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    user = User(
        username=data['username'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado"})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(
            identity=str(user.id),  # ✅ AGORA É STRING
            additional_claims={"role": user.role}
        )
        return jsonify(access_token=token)

    return jsonify({"msg": "Credenciais inválidas"}), 401