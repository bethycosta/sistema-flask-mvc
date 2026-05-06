from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()

    data = request.json

    product = Product(
        nome=data['nome'],
        preco=data['preco'],
        user_id=user_id
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"msg": "Produto criado"})


@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    produtos = Product.query.all()

    return jsonify([
        {"id": p.id, "nome": p.nome, "preco": p.preco}
        for p in produtos
    ])


@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    user_id = get_jwt_identity()
    claims = get_jwt()

    product = Product.query.get(id)

    if not product:
        return jsonify({"msg": "Produto não encontrado"}), 404

    if claims["role"] != "admin" and str(product.user_id) != user_id:
        return jsonify({"msg": "Sem permissão"}), 403

    data = request.json
    product.nome = data['nome']
    product.preco = data['preco']

    db.session.commit()

    return jsonify({"msg": "Atualizado"})


@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    claims = get_jwt()

    product = Product.query.get(id)

    if not product:
        return jsonify({"msg": "Produto não encontrado"}), 404

    if claims["role"] != "admin":
        return jsonify({"msg": "Somente admin"}), 403

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg": "Deletado"})