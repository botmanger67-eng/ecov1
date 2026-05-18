import React, { useState, useEffect, useContext } from 'react';
import { CartContext } from '../App';

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image: string;
}

const Cart: React.FC = () => {
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { cartCount, updateCartCount } = useContext(CartContext);

  useEffect(() => {
    fetchCartItems();
  }, []);

  const fetchCartItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/cart', { credentials: 'include' });
      if (!response.ok) {
        throw new Error('Failed to fetch cart items');
      }
      const data: CartItem[] = await response.json();
      setItems(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleQuantityChange = async (id: number, delta: number) => {
    const item = items.find(i => i.id === id);
    if (!item) return;
    const newQuantity = item.quantity + delta;
    if (newQuantity < 1) return;
    try {
      const response = await fetch(`/api/cart/update/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: newQuantity }),
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to update quantity');
      }
      setItems(prev =>
        prev.map(i => (i.id === id ? { ...i, quantity: newQuantity } : i))
      );
      updateCartCount();
    } catch (err: any) {
      setError(err.message || 'Update failed');
    }
  };

  const handleRemoveItem = async (id: number) => {
    try {
      const response = await fetch(`/api/cart/remove/${id}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to remove item');
      }
      setItems(prev => prev.filter(i => i.id !== id));
      updateCartCount();
    } catch (err: any) {
      setError(err.message || 'Remove failed');
    }
  };

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  if (loading) return <div className="cart-loading">Loading cart...</div>;
  if (error) return <div className="cart-error">Error: {error}</div>;

  return (
    <div className="cart">
      <h2>Your Shopping Cart</h2>
      {items.length === 0 ? (
        <p className="cart-empty">Your cart is empty.</p>
      ) : (
        <div className="cart-items">
          {items.map(item => (
            <div key={item.id} className="cart-item">
              <img src={item.image} alt={item.name} className="cart-item-image" />
              <div className="cart-item-details">
                <h3>{item.name}</h3>
                <p className="cart-item-price">${item.price.toFixed(2)}</p>
                <div className="cart-item-quantity">
                  <button onClick={() => handleQuantityChange(item.id, -1)} disabled={item.quantity <= 1}>
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button onClick={() => handleQuantityChange(item.id, 1)}>+</button>
                </div>
                <p className="cart-item-subtotal">Subtotal: ${(item.price * item.quantity).toFixed(2)}</p>
                <button className="cart-item-remove" onClick={() => handleRemoveItem(item.id)}>
                  Remove
                </button>
              </div>
            </div>
          ))}
          <div className="cart-total">
            <strong>Total: ${total.toFixed(2)}</strong>
          </div>
          <a href="/checkout" className="cart-checkout-btn">Proceed to Checkout</a>
        </div>
      )}
    </div>
  );
};

export default Cart;