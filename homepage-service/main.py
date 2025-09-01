from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Sample product data (in production, this would come from a database)
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "High-performance laptop"},
    {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest smartphone"},
    {"id": 3, "name": "Headphones", "price": 99.99, "description": "Wireless headphones"},
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "products": products}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
