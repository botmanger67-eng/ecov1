# E-Commerce Platform

A full-stack e-commerce website built with React, Flask, and SQLite. This project provides a simple, functional online store with product listing, shopping cart, and checkout capabilities.

## Features

- **Product Listing** – Browse a catalog of products with details and pricing.
- **Shopping Cart** – Add, remove, and update product quantities in the cart.
- **Checkout Process** – Complete a purchase flow (simulated) with order summary.
- **RESTful API** – Backend powered by Flask, serving product and order data.
- **Persistent Storage** – SQLite database for products, carts, and orders.
- **Responsive UI** – Modern, clean interface built with React.

## Tech Stack

| Layer       | Technology             |
|-------------|------------------------|
| Frontend    | React, CSS             |
| Backend     | Flask (Python)         |
| Database    | SQLite                 |
| Other       | npm (Node.js), pip     |

## Installation

### Prerequisites
- Python 3.8+
- Node.js and npm
- Git

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ecommerce-platform
   ```
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
4. Install Python dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
5. Initialize the database (run once):
   ```bash
   python app.py
   ```
   (The app will create the SQLite database file and tables automatically.)

### Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```

## Usage

### Start the Backend Server
From the `backend` directory (with virtual environment activated):
```bash
python app.py
```
The Flask server will start on `http://localhost:5000`.

### Start the Frontend Server
From the `frontend` directory:
```bash
npm start
```
The React development server will run on `http://localhost:3000`. Open this URL in your browser to use the platform.

> **Note:** The frontend is configured to proxy API requests to the Flask backend (port 5000). Ensure both servers are running simultaneously.

## Project Structure

```
ecommerce-platform/
├── backend/
│   ├── app.py          # Main Flask application entry point
│   ├── models.py       # SQLAlchemy models (Product, Cart, Order)
│   ├── routes.py       # API endpoints (products, cart, checkout)
│   └── config.py       # Configuration settings (database URI, etc.)
├── frontend/
│   ├── public/
│   │   └── index.html  # HTML template
│   ├── src/
│   │   ├── App.js      # Main React component
│   │   ├── App.css     # Global styles
│   │   ├── components/
│   │   │   ├── ProductList.js   # Product listing component
│   │   │   ├── Cart.js          # Shopping cart component
│   │   │   └── Checkout.js      # Checkout component
│   └── package.json    # Node dependencies and scripts
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.