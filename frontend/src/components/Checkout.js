import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';

const Checkout = ({ cartItems, total, onOrderPlaced }) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    country: 'US',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const validate = () => {
    const newErrors = {};
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone is required';
    } else if (!/^\d{10,15}$/.test(formData.phone.replace(/[\s\-\(\)]/g, ''))) {
      newErrors.phone = 'Invalid phone number (10-15 digits)';
    }
    if (!formData.address.trim()) newErrors.address = 'Address is required';
    if (!formData.city.trim()) newErrors.city = 'City is required';
    if (!formData.state.trim()) newErrors.state = 'State is required';
    if (!formData.zip.trim()) {
      newErrors.zip = 'ZIP code is required';
    } else if (!/^\d{5}(-\d{4})?$/.test(formData.zip)) {
      newErrors.zip = 'Invalid ZIP code';
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    if (!cartItems || cartItems.length === 0) {
      setSubmitError('Your cart is empty');
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '',
        },
        body: JSON.stringify({
          shipping: formData,
          items: cartItems.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price,
          })),
          total,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Checkout failed (${response.status})`);
      }

      const result = await response.json();
      if (onOrderPlaced) {
        onOrderPlaced(result.order_id);
      }
      navigate('/order-confirmation', { state: { orderId: result.order_id } });
    } catch (error) {
      setSubmitError(error.message || 'An unexpected error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const inputClass = (fieldName) =>
    `checkout-input ${errors[fieldName] ? 'checkout-input--error' : ''}`;

  return (
    <div className="checkout">
      <h2>Checkout</h2>
      {submitError && <div className="checkout-error">{submitError}</div>}
      <form onSubmit={handleSubmit} noValidate>
        <div className="checkout-section">
          <h3>Contact Information</h3>
          <div className="checkout-row">
            <div className="checkout-field">
              <label htmlFor="firstName">First Name *</label>
              <input
                id="firstName"
                className={inputClass('firstName')}
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                required
              />
              {errors.firstName && <span className="checkout-field-error">{errors.firstName}</span>}
            </div>
            <div className="checkout-field">
              <label htmlFor="lastName">Last Name *</label>
              <input
                id="lastName"
                className={inputClass('lastName')}
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                required
              />
              {errors.lastName && <span className="checkout-field-error">{errors.lastName}</span>}
            </div>
          </div>
          <div className="checkout-row">
            <div className="checkout-field">
              <label htmlFor="email">Email *</label>
              <input
                id="email"
                className={inputClass('email')}
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              {errors.email && <span className="checkout-field-error">{errors.email}</span>}
            </div>
            <div className="checkout-field">
              <label htmlFor="phone">Phone *</label>
              <input
                id="phone"
                className={inputClass('phone')}
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
              />
              {errors.phone && <span className="checkout-field-error">{errors.phone}</span>}
            </div>
          </div>
        </div>

        <div className="checkout-section">
          <h3>Shipping Address</h3>
          <div className="checkout-field">
            <label htmlFor="address">Address *</label>
            <input
              id="address"
              className={inputClass('address')}
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
            />
            {errors.address && <span className="checkout-field-error">{errors.address}</span>}
          </div>
          <div className="checkout-row">
            <div className="checkout-field">
              <label htmlFor="city">City *</label>
              <input
                id="city"
                className={inputClass('city')}
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                required
              />
              {errors.city && <span className="checkout-field-error">{errors.city}</span>}
            </div>
            <div className="checkout-field">
              <label htmlFor="state">State *</label>
              <input
                id="state"
                className={inputClass('state')}
                type="text"
                name="state"
                value={formData.state}
                onChange={handleChange}
                required
              />
              {errors.state && <span className="checkout-field-error">{errors.state}</span>}
            </div>
          </div>
          <div className="checkout-row">
            <div className="checkout-field">
              <label htmlFor="zip">ZIP Code *</label>
              <input
                id="zip"
                className={inputClass('zip')}
                type="text"
                name="zip"
                value={formData.zip}
                onChange={handleChange}
                required
              />
              {errors.zip && <span className="checkout-field-error">{errors.zip}</span>}
            </div>
            <div className="checkout-field">
              <label htmlFor="country">Country</label>
              <select
                id="country"
                className="checkout-input"
                name="country"
                value={formData.country}
                onChange={handleChange}
              >
                <option value="US">United States</option>
                <option value="CA">Canada</option>
                <option value="MX">Mexico</option>
              </select>
            </div>
          </div>
        </div>

        <div className="checkout-summary">
          <h3>Order Summary</h3>
          <p>Items: {cartItems ? cartItems.length : 0}</p>
          <p>Total: ${total ? total.toFixed(2) : '0.00'}</p>
        </div>

        <button
          type="submit"
          className="checkout-submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Processing...' : 'Place Order'}
        </button>
      </form>
    </div>
  );
};

Checkout.propTypes = {
  cartItems: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      quantity: PropTypes.number.isRequired,
      price: PropTypes.number.isRequired,
    })
  ),
  total: PropTypes.number,
  onOrderPlaced: PropTypes.func,
};

Checkout.defaultProps = {
  cartItems: [],
  total: 0,
  onOrderPlaced: null,
};

export default Checkout;