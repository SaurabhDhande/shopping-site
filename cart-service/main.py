from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cart data structure (in production, this would be in a database)
cart = {}

class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/cart")
async def get_cart():
    return cart

@app.post("/cart/add")
async def add_to_cart(item: CartItem):
    if item.product_id in cart:
        cart[item.product_id] += item.quantity
    else:
        cart[item.product_id] = item.quantity
    return {"message": "Item added to cart", "cart": cart}

@app.delete("/cart/{product_id}")
async def remove_from_cart(product_id: int):
    if product_id in cart:
        del cart[product_id]
        return {"message": "Item removed from cart", "cart": cart}
    return {"message": "Item not found in cart"}

@app.get("/cart-view", response_class=HTMLResponse)
async def cart_view(request: Request):
    return templates.TemplateResponse(
        "cart.html",
        {"request": request}
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
