from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import auth, users, contact, slider, trainer, admin, product
from api.database.connection import engine
from api.database.base import Base

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Serve static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")  # Serve images

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include authentication-related routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Include user-related routes
app.include_router(users.router, prefix="/users", tags=["Users"])


app.include_router(contact.router, prefix="/contact", tags=["Contact"])

app.include_router(slider.router, prefix="/slider", tags=["Slider"])


app.include_router(trainer.router, prefix="/trainer", tags=["Trainer"])


app.include_router(admin.router, prefix="/admin", tags=["AdminDetails"])


app.include_router(product.router, prefix="/product", tags=["Product"])
