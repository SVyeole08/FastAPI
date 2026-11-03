# Stockroom : Frontend

A React-based inventory dashboard for **Stockroom**, a full-stack inventory management application. The frontend lets
users view, search, add, edit, and delete products while displaying useful inventory statistics. It communicates with a
FastAPI backend connected to PostgreSQL.

**Live:** https://fastapi-1-pgri.onrender.com

## Functionalities

- **Inventory overview:** View products in a structured dashboard.
- **Inventory statistics:** See the number of listed products, total units in stock, estimated inventory value, and
  low-stock count.
- **Product search:** Filter products by name, description, or product ID.
- **Add products:** Create inventory entries with an ID, name, description, price, and quantity.
- **Edit products:** Update existing product details. Product IDs remain unchanged when editing.
- **Delete products:** Remove products from the inventory after confirmation.
- **Stock indicators:** Identify low, medium, and healthy stock levels.
- **Live API data:** Load and refresh inventory data from the FastAPI backend.
- **Error handling:** Display backend connection or request errors and provide a retry option.
- **Responsive interface elements:** Use a dashboard layout with product actions, forms, and status indicators.

## Tech Stack

| Technology               | Purpose                                 |
|--------------------------|-----------------------------------------|
| React 18                 | UI and component-based application      |
| Vite 6                   | Development server and production build |
| JavaScript (ES6 modules) | Frontend application logic              |
| Lucide React             | Interface icons                         |
| CSS                      | Dashboard styling                       |
| Fetch API                | HTTP requests to the backend            |

## Frontend Structure

```text
frontend/
├── index.html          # HTML entry point
├── package.json        # Dependencies and npm scripts
├── vite.config.js      # Vite configuration and development API proxy
└── src/
    ├── main.jsx        # React app, inventory UI, and API interactions
    └── styles.css      # Application styles
```

## Backend Integration

The frontend retrieves and manages inventory through the Stockroom FastAPI API.

| Method   | Endpoint           | Frontend use           |
|----------|--------------------|------------------------|
| `GET`    | `/products`        | Fetch the product list |
| `POST`   | `/product`         | Add a product          |
| `PUT`    | `/product?id={id}` | Update a product       |
| `DELETE` | `/product?id={id}` | Delete a product       |

The frontend expects product records containing:

```json
{
  "id": 1,
  "name": "Wireless headphones",
  "description": "Bluetooth headphones",
  "price": 2499,
  "quantity": 12
}
```

Prices are displayed in Indian rupees (₹). Inventory value is calculated from each product’s price multiplied by its
available quantity. The dashboard marks stock of **5 units or fewer** as low.