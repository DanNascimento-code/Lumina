from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, qty: int | None = None):
    if qty:
        return {"item_id": item_id, "qty": qty}
    return {"item_id": item_id}



