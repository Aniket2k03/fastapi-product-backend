from fastapi import FastAPI, Depends
from models import Product
from fastapi.middleware.cors import CORSMiddleware
from database import session
import database_models
from database import engine
from sqlalchemy.orm import Session
app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.get("/")
def greet():
    return "Welcome to the product inventory!"

Products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=5),
    Product(id=2, name="laptop", description="budget laptop", price=999, quantity=10),
    Product(id=3, name="pen", description="blue ink pen", price=10, quantity=100),
    Product(id=4, name="table", description="wooden study table", price=1500, quantity=3)
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = session()   # 1️⃣ Open a new database session

    # 2️⃣ Count how many products already exist
    count = db.query(database_models.Product).count()

    # 3️⃣ If no products exist, add the default ones
    if count == 0:
        for product in Products:
            db.add(database_models.Product(**product.model_dump()))  # 4️⃣ Insert product into DB

    db.commit()   # 5️⃣ Save changes to DB

# Call the function to initialize DB
init_db()



@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/products/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        return db_products
    return "Product Not Found"
    

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))  # 4️⃣ Insert product into DB
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()        
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return "Product Updated Successfully !"
    else:
        return "No Product Found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "Product Deleted"
    else:
        return "Product Not Found"