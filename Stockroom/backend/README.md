# Stockroom : Backend API

The backend for **Stockroom**, a full-stack inventory management application. It provides a REST API built with FastAPI
and SQLAlchemy, with PostgreSQL used to persist product inventory data.

**Live API:** https://fastapi-0sk4.onrender.com <br/>
**API documentation:** https://fastapi-0sk4.onrender.com/docs

## Functions

- **REST API:** Endpoints to create, retrieve, update, and delete inventory products.
- **PostgreSQL integration:** Store product records in a relational database.
- **SQLAlchemy ORM:** Map Python product models to the database table.
- **Pydantic validation:** Validate product data received by the API.
- **Database initialization:** Create the products table when the application starts and add sample products if the
  table is empty.
- **CORS configuration:** Allow requests from the deployed Stockroom frontend.
- **Swagger UI:** Explore and test API endpoints through FastAPI’s interactive documentation.

## Tech Stack

| Technology | Purpose                        |
|------------|--------------------------------|
| Python     | Backend programming language   |
| FastAPI    | REST API framework             |
| SQLAlchemy | ORM and database operations    |
| PostgreSQL | Persistent relational database |
| Pydantic   | Request data validation        |
| Psycopg2   | PostgreSQL database driver     |
| Uvicorn    | ASGI server                    |

## Backend Structure

```text
backend/
├── main.py               # FastAPI application, routes, CORS, and DB initialization
├── database.py           # PostgreSQL engine and SQLAlchemy session configuration
├── database_models.py    # SQLAlchemy Base and Product table model
├── models.py              # Pydantic Product request model
└── requirements.txt       # Python dependencies
```

## Product Data Model

The API manages products with the following fields:

| Field         | Type    | Description                        |
|---------------|---------|------------------------------------|
| `id`          | Integer | Product identifier and primary key |
| `name`        | String  | Product name                       |
| `description` | String  | Product description                |
| `price`       | Float   | Product price                      |
| `quantity`    | Integer | Available stock quantity           |

Example product payload:

```json
{
  "id": 3,
  "name": "Wireless headphones",
  "description": "Bluetooth headphones",
  "price": 2499,
  "quantity": 12
}
```

The product ID is supplied in the request body; the current API model does not define it as automatically generated.

## API Endpoints

Base URL: `https://fastapi-0sk4.onrender.com`

| Method   | Endpoint           | Description              |
|----------|--------------------|--------------------------|
| `GET`    | `/`                | Return a welcome message |
| `GET`    | `/products`        | Retrieve all products    |
| `GET`    | `/product/{id}`    | Retrieve a product by ID |
| `POST`   | `/product`         | Add a product            |
| `PUT`    | `/product?id={id}` | Update a product by ID   |
| `DELETE` | `/product?id={id}` | Delete a product by ID   |
