from fastapi import FastAPI
from pydantic import BaseModel

from models import Product
from database import session, engine
from database_models import Base
from database_models import Product as prd

Base.metadata.create_all(engine)
app = FastAPI()

Products = [
    Product(id=1, name="Realme-P3X", description="Budget 5G Phone", price=11500, quantity=20),
    Product(id=2, name="HP-Elitebook-840-G6", description="Refurbished Working laptop", price=26000, quantity=5),
]


def init_db():
    db = session
    count = db.query(prd).count
    if count == 0:
        for product in Products:
            db.add(prd(**product.model_dump()))
        db.commit()

init_db()


# get method is used only to read the data which is been already uploaded
@app.get("/")
def welcome():
    return "Welcome to the FastAPI"


@app.get("/products")
def get_products():
    # DB = session()
    # DB.query()
    return Products


@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in Products:
        if product.id == id:
            return product

    return "Product not found"


# post method is used to add data
@app.post("/product")
def add_product(product: Product):
    Products.append(product)
    return f"Product got added successfully | len(Products) = {len(Products)}"


# put method is used to update data
@app.put("/product")
def update_product(id: int, product: Product):
    for pid in range(len(Products)):
        if Products[pid].id == id:
            Products[pid] = product
            return f"Product of id {id} got updated successfully."

    return "Product not found"


# delete method is used to delete data
@app.delete("/product")
def delete_product(id: int):
    for pid in range(len(Products)):
        if Products[pid].id == id:
            del Products[pid]
            return f"Product of id {id} got deleted successfully"

    return "Product not found"
