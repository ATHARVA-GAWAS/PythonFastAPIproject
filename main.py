from fastapi import FastAPI, HTTPException
import asyncpg
from pydantic import BaseModel
from fastapi.responses import FileResponse

# Create a FastAPI instance
app = FastAPI()

# Database connection pool
pool = None

# Model for the data
class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")    


# Function to initialize database connection pool
async def get_pool():
    if pool is None:
        pool = await asyncpg.create_pool(user='postgres', password='postgres',
                                         database='apidatabase', host='localhost')
    return app.state.pool

# Create operation
@app.post("/")
async def create_item(item: Item):
    query = "INSERT INTO items(name, description, price) VALUES($1, $2, $3) RETURNING id"
    async with get_pool() as pool:
        async with pool.acquire() as con:
            item_id = await con.fetchval(query, item.name, item.description, item.price)
    return {"id": item_id, **item.dict()}

# Read operation
@app.get("/")
async def read_items():
    query = "SELECT * FROM items"
    async with get_pool() as pool:
        async with pool.acquire() as con:
            rows = await con.fetch(query)
            return [dict(row) for row in rows]

# Update operation
@app.put("/update/{item_id}")
async def update_item(item_id: int, item: Item):
    query = "UPDATE items SET name=$1, description=$2, price=$3 WHERE id=$4"
    async with get_pool() as pool:
        async with pool.acquire() as con:
            await con.execute(query, item.name, item.description, item.price, item_id)
    return {"id": item_id, **item.dict()}

# Delete operation
@app.delete("/delete/{item_id}")
async def delete_item(item_id: int):
    query = "DELETE FROM items WHERE id = $1"
    async with get_pool() as pool:
        async with pool.acquire() as con:
            await con.execute(query, item_id)
    return {"message": "Item deleted successfully"}
