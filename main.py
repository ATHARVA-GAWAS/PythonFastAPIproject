import sys
print(sys.path)

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from api import models, crud
from db.database import Base
from fastapi.responses import HTMLResponse


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("./static/index.html", "r") as file:
        html_content = file.read()
    return html_content

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=models.Item)
def create_item(item: models.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[models.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)

@app.get("/items/{item_id}", response_model=models.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_items(db=db, item_id=item_id)

@app.put("/items/{item_id}", response_model=models.Item)
def update_item(item_id: int, item: models.ItemCreate, db: Session = Depends(get_db)):
    return crud.update_item(db=db, item_id=item_id, item=item)

@app.delete("/items/{item_id}", response_model=models.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db=db, item_id=item_id)