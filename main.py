import uvicorn
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
#from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor



app = FastAPI()

#FastAPIInstrumentor.instrument_app(app)

class Item(BaseModel):
    id: int
    description: str
    dueDate: Union[str, None] = None


todos = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todo")
def get_items() -> dict:
    return { "data" : todos}

@app.post("/todo")
async def add_item(item: Item):
    todos[item.id] = item
    return todos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)