# Stockroom (Inventory Management System)

A full-stack inventory management application built with **FastAPI, PostgreSQL, SQLAlchemy, React, and Vite**. Stockroom
provides a dashboard for managing products, monitoring stock quantities, and calculating inventory value.

## 🌐 Live Project

- **Frontend:** [Stockroom Inventory Dashboard](https://fastapi-1-pgri.onrender.com)
- **Backend API:** [FastAPI Backend](https://fastapi-0sk4.onrender.com)
- **API Documentation:** [Swagger UI](https://fastapi-0sk4.onrender.com/docs)

## Features

### Inventory dashboard

- View all products in the inventory.
- See the number of products and total units in stock.
- Calculate total inventory value from product price × quantity.
- Identify low-stock products (quantity of 5 or fewer).
- Search products by name, description, or ID.

### Product management

- Add products with an ID, name, description, price, and quantity.
- Edit existing product details.
- Delete products from the inventory.
- Refresh the product list from the backend.

### API

- REST endpoints built with FastAPI.
- PostgreSQL persistence using SQLAlchemy.
- Request and response data handled with Pydantic models.
- Interactive API documentation provided by FastAPI.

## Tech Stack

| Layer      | Technologies                               |
|------------|--------------------------------------------|
| Frontend   | React, Vite, JavaScript, CSS, Lucide React |
| Backend    | Python, FastAPI, Uvicorn, Pydantic         |
| Database   | PostgreSQL                                 |
| ORM        | SQLAlchemy                                 |
| Deployment | Render (backend, frontend, and PostgreSQL) |

## Repository Structure

```text
FastAPI/
├── backend/
│   ├── main.py              # FastAPI app and product API routes
│   ├── database.py          # PostgreSQL connection and SQLAlchemy session
│   ├── database_models.py   # SQLAlchemy Product table model
│   ├── models.py            # Pydantic Product schema
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx         # React app and inventory UI
│   │   └── styles.css       # Dashboard styling
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js       # Vite development configuration
│
└── .gitignore
```

## Database Model

The application stores products in a PostgreSQL table named `products`.

| Column        | Type                 | Description              |
|---------------|----------------------|--------------------------|
| `id`          | Integer, primary key | Product identifier       |
| `name`        | String               | Product name             |
| `description` | String               | Product description      |
| `price`       | Float                | Product price            |
| `quantity`    | Integer              | Available stock quantity |

The SQLAlchemy model is defined in `backend/database_models.py`. The Pydantic schema in `backend/models.py` defines the
product data expected by the API.

On backend startup, the application creates the table if it does not exist. If the table is empty, it inserts two sample
products.

## API Endpoints

The API is implemented in `backend/main.py`.

| Method   | Endpoint           | Purpose                   |
|----------|--------------------|---------------------------|
| `GET`    | `/`                | Returns a welcome message |
| `GET`    | `/products`        | Returns all products      |
| `GET`    | `/product/{id}`    | Returns a product by ID   |
| `POST`   | `/product`         | Adds a product            |
| `PUT`    | `/product?id={id}` | Updates a product         |
| `DELETE` | `/product?id={id}` | Deletes a product         |

### Example product JSON

```json
{
  "id": 1,
  "name": "Realme-P4X",
  "description": "Budget 5G Phone",
  "price": 11500,
  "quantity": 20
}
```

### Create a product

Send a `POST` request to `/product` with a JSON body containing all five fields, including the product ID.

### Update a product

Send a `PUT` request to `/product?id=1` with the product data in the request body.

### Delete a product

Send a `DELETE` request to `/product?id=1`.

> **Note:** The current API expects the product ID to be supplied by the client when creating a product. It does not
> automatically generate IDs.

## Project Overview

I built Stockroom while learning **FastAPI** as a hands-on project to apply concepts such as REST API development, database integration with PostgreSQL and SQLAlchemy, and connecting a backend to a React frontend. It helped me understand how these technologies work together in a full-stack application.