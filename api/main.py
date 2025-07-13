from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
# Log startup to Vercel logs
print("🚀 FastAPI app starting...")

# ----------------------------------------------------------------------------
# FASTAPI APPLICATION INITIALIZATION
# ----------------------------------------------------------------------------
app = FastAPI()

# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")  # Serve static files

if os.path.isdir("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
else:
    print("⚠️ Warning: 'uploads' directory not found, skipping static mount.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------------------------------
try:
    from api.database.connection import engine
    from api.database.base import Base

    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized.")
except Exception as db_error:
    print("❌ Database Initialization Error:", db_error)

# ----------------------------------------------------------------------------
# ROUTES IMPORT & SETUP
# ----------------------------------------------------------------------------
try:
    from api.routes import auth, users, contact, slider, trainer, admin, product

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(contact.router, prefix="/contact", tags=["Contact"])
    app.include_router(slider.router, prefix="/slider", tags=["Slider"])
    app.include_router(trainer.router, prefix="/trainer", tags=["Trainer"])
    app.include_router(admin.router, prefix="/admin", tags=["AdminDetails"])
    app.include_router(product.router, prefix="/product", tags=["Product"])

    print("✅ Routers loaded successfully.")
except Exception as route_error:
    print("❌ Router Import Error:", route_error)

# ----------------------------------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "✅ FastAPI main.py is working correctly"}
