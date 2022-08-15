import uvicorn
import logging
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from prometheusrock import PrometheusMiddleware, metrics_route
#from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor





app = FastAPI()
#Add Prometheus Support
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics_route)

#Otel Instrumentor
#FastAPIInstrumentor.instrument_app(app)

# Add Logging Config 
log = logging.getLogger(__name__)
FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

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
    log.debug("Request for todos")
    return { "data" : todos}

@app.post("/todo")
async def add_item(item: Item):
    todos[item.id] = item
    log.debug("Add item to todo list")
    return todos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)