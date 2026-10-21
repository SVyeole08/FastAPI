from fastapi import FastAPI
from models import Product

app = FastAPI()

Products = [
    Product(id=1, name="Realme-P3X", desc="Budget 5G Phone", price=11500, qty=20),
    Product(id=2, name="HP-Elitebook-840-G6", desc="Refurbished Working laptop", price=26000, qty=5),
]


# get method is used only to read the data which is been already uploaded
@app.get("/")
def welcome():
    return "Welcome to the FastAPI"


@app.get("/products")
def get_products():
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
