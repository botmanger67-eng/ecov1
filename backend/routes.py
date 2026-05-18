from flask import Blueprint, request, jsonify, session
from backend.models import db, Product, CartItem, Order
from backend.config import Config
import traceback

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve all products.
    Returns: JSON with list of products.
    """
    try:
        products = Product.query.all()
        product_list = [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'image_url': p.image_url,
            'stock': p.stock
        } for p in products]
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch products', 'details': str(e)}), 500

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    """
    Get a single product by ID.
    Returns: JSON product or 404.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'image_url': product.image_url,
            'stock': product.stock
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch product', 'details': str(e)}), 500

@api.route('/cart', methods=['GET'])
def get_cart():
    """
    Get current user's cart items.
    Uses session to identify user (default user_id=1 if not set).
    Returns: JSON array of cart items.
    """
    try:
        user_id = session.get('user_id', 1)  # fallback to demo user
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        items = [{
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': float(item.product.price)
            }
        } for item in cart_items]
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch cart', 'details': str(e)}), 500

@api.route('/cart', methods=['POST'])
def add_to_cart():
    """
    Add item to cart.
    Expects JSON: { "product_id": int, "quantity": int }
    Updates quantity if product already in cart.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        if not product_id or not isinstance(quantity, int) or quantity < 1:
            return jsonify({'error': 'Invalid product_id or quantity'}), 400
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        if product.stock < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        user_id = session.get('user_id', 1)
        existing_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            if existing_item.quantity > product.stock:
                return jsonify({'error': 'Total quantity exceeds stock'}), 400
        else:
            new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_item)
        
        db.session.commit()
        return jsonify({'message': 'Item added to cart'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add item to cart', 'details': str(e)}), 500

@api.route('/cart/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id: int):
    """
    Update quantity of a cart item.
    Expects JSON: { "quantity": int }
    """
    try:
        data = request.get_json()
        if not data or 'quantity' not in data:
            return jsonify({'error': 'Missing quantity field'}), 400
        quantity = data['quantity']
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({'error': 'Quantity must be non-negative integer'}), 400
        
        user_id = session.get('user_id', 1)
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        if quantity == 0:
            db.session.delete(cart_item)
        else:
            product = Product.query.get(cart_item.product_id)
            if product.stock < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            cart_item.quantity = quantity
        
        db.session.commit()
        return jsonify({'message': 'Cart item updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update cart item', 'details': str(e)}), 500

@api.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id: int):
    """
    Remove a cart item.
    """
    try:
        user_id = session.get('user_id', 1)
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Cart item removed'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove cart item', 'details': str(e)}), 500

@api.route('/checkout', methods=['POST'])
def checkout():
    """
    Process checkout: create order from cart items, reduce stock, clear cart.
    Expects optional JSON: { "shipping_address": str } (default "Default Address")
    """
    try:
        data = request.get_json() or {}
        shipping_address = data.get('shipping_address', 'Default Address')
        user_id = session.get('user_id', 1)
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total_price = 0.0
        order_items = []
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                continue
            if product.stock < item.quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            # Reduce stock
            product.stock -= item.quantity
            total_price += product.price * item.quantity
            order_items.append({
                'product_id': product.id,
                'quantity': item.quantity,
                'price': float(product.price)
            })
        
        # Create order
        shipping_cost = 0.0  # could be configurable
        order = Order(
            user_id=user_id,
            total_price=total_price + shipping_cost,
            shipping_address=shipping_address,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # get order.id
        
        # Optionally store order items in a separate table if exists; but we skip for brevity
        # Clear cart
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': order.id,
            'total': total_price + shipping_cost
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Checkout failed', 'details': str(e)}), 500