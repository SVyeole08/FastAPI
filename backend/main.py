from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from models import Product
from database import SessionLocal, engine
from database_models import Base
from database_models import Product as prd

Base.metadata.create_all(engine)
app = FastAPI()

Products = [
    Product(id=1, name="Realme-P3X", description="Budget 5G Phone", price=11500, quantity=20),
    Product(id=2, name="HP-Elitebook-840-G6", description="Refurbished Working laptop", price=26000, quantity=5),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    count = db.query(prd).count()
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
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(prd).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(prd).filter(prd.id == id).first()
    if db_product:
        return db_product

    return "Product not found"


# post method is used to add data
@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(prd(**product.model_dump()))
    db.commit()
    return f"Product got added successfully | Count of Products = {db.query(prd).count()}"


# put method is used to update data
@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(prd).filter(prd.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return f"Product of id {id} got updated"
    return "Product not found"


# delete method is used to delete data
@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(prd).filter(prd.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return f"Product of id {id} got deleted"
    return "Product not found"
