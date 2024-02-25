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
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRUD API Frontend</title>
    <style>

    </style>
</head>
<body>
    <h1>CRUD API Frontend</h1>
    

    <h2>Create Item</h2>
    <form id="create-form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="description">Description:</label>
        <input type="text" id="description" name="description">
        <label for="price">Price:</label>
        <input type="number" id="price" name="price" step="0.01" required>
        <label for="tax">Tax:</label>
        <input type="number" id="tax" name="tax" step="0.01">
        <button type="submit">Create</button>
    </form>
    

    <h2>Items</h2>
    <ul id="item-list"></ul>
    
    <h2>Update Item</h2>
    <form id="update-form" style="display: none;">
        <input type="hidden" id="update-id" name="id">
        <label for="update-name">Name:</label>
        <input type="text" id="update-name" name="name" required>
        <label for="update-description">Description:</label>
        <input type="text" id="update-description" name="description">
        <label for="update-price">Price:</label>
        <input type="number" id="update-price" name="price" step="0.01" required>
        <label for="update-tax">Tax:</label>
        <input type="number" id="update-tax" name="tax" step="0.01">
        <button type="submit">Update</button>
        <button id="cancel-update" type="button">Cancel</button>
    </form>
    

    <h2>Delete Item</h2>
    <input type="number" id="delete-id" name="id" placeholder="Enter ID">
    <button id="delete-button" type="button">Delete</button>
    
    <script>

        async function fetchItems() {
            const response = await fetch('http://localhost:8000/items');
            const data = await response.json();
            const itemList = document.getElementById('item-list');
            itemList.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.id}: ${item.name}, Price: ${item.price}`;
                itemList.appendChild(li);
            });
        }

        async function createItem(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            await fetch('http://localhost:8000/items', {
                method: 'POST',
                body: formData
            });
            fetchItems();
            event.target.reset();
        }


        async function updateItem(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const itemId = formData.get('id');
            await fetch(`http://localhost:8000/items/${itemId}`, {
                method: 'PUT',
                body: formData
            });
            fetchItems();
            event.target.reset();
            document.getElementById('update-form').style.display = 'none';
        }


        function cancelUpdate() {
            document.getElementById('update-form').style.display = 'none';
        }


        async function deleteItem() {
            const itemId = document.getElementById('delete-id').value;
            await fetch(`http://localhost:8000/items/${itemId}`, {
                method: 'DELETE'
            });
            fetchItems();
            document.getElementById('delete-id').value = '';
        }

        document.getElementById('create-form').addEventListener('submit', createItem);
        document.getElementById('update-form').addEventListener('submit', updateItem);
        document.getElementById('cancel-update').addEventListener('click', cancelUpdate);
        document.getElementById('delete-button').addEventListener('click', deleteItem);

        fetchItems();
    </script>
</body>
</html>
    """
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