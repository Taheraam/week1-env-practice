from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

app = FastAPI()

db: dict[int, dict] = {}
next_id: int = 1

class Item(BaseModel):
    name: str
    price: float

@app.post('/items', status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> dict:
    global next_id
    db[next_id] = item.model_dump()
    db[next_id]['id'] = next_id
    next_id += 1
    return db[next_id - 1]

@app.get('/items/{item_id}')
def get_item(item_id: int) -> dict:
    if item_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {item_id} not found'
        )
    return db[item_id]

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item) -> dict:
    if item_id not in db:
        raise HTTPException(status_code=404, detail='Not found')
    db[item_id].update(item.model_dump())
    return db[item_id]

@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if item_id not in db:
        raise HTTPException(status_code=404, detail='Not found')
    del db[item_id]