from datetime import datetime, timezone
from typing import List, Optional
from backend.app import db


class User(db.Model):
    """User model for authentication and profile."""

    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email: str = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(128), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    cart_items: List['CartItem'] = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders: List['Order'] = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Product(db.Model):
    """Product model representing an item in the store."""

    __tablename__ = 'products'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False, index=True)
    description: str = db.Column(db.Text, nullable=True)
    price: float = db.Column(db.Float, nullable=False)
    stock_quantity: int = db.Column(db.Integer, nullable=False, default=0)
    image_url: str = db.Column(db.String(500), nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    cart_items: List['CartItem'] = db.relationship('CartItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items: List['OrderItem'] = db.relationship('OrderItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Product {self.name}>'


class CartItem(db.Model):
    """Model representing a product added to a user's shopping cart."""

    __tablename__ = 'cart_items'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id: int = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False, default=1)
    added_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uq_user_product_cart'),
    )

    def __repr__(self) -> str:
        return f'<CartItem user={self.user_id} product={self.product_id} qty={self.quantity}>'


class Order(db.Model):
    """Order model representing a completed purchase."""

    __tablename__ = 'orders'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price: float = db.Column(db.Float, nullable=False, default=0.0)
    status: str = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid, shipped, delivered, cancelled
    shipping_address: str = db.Column(db.Text, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    items: List['OrderItem'] = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Order {self.id} user={self.user_id} status={self.status}>'


class OrderItem(db.Model):
    """Model representing a single product line in an order."""

    __tablename__ = 'order_items'

    id: int = db.Column(db.Integer, primary_key=True)
    order_id: int = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id: int = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)
    unit_price: float = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f'<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>'