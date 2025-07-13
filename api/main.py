from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# ----------------------------------------------------------------------------
# ASGI LIFESPAN CONTEXT
# ----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔁 App is starting...")

    # Database initialization
    try:
        from api.database.connection import engine
        from api.database.base import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables initialized.")
    except Exception as db_error:
        print("❌ Database Initialization Error:", db_error)

    # Router imports
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

    yield  # Application runs here

    print("🛑 App is shutting down...")  # On shutdown

# ----------------------------------------------------------------------------
# FASTAPI APPLICATION INITIALIZATION
# ----------------------------------------------------------------------------
app = FastAPI(lifespan=lifespan)

# ----------------------------------------------------------------------------
# STATIC FILES SETUP
# ----------------------------------------------------------------------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")  # Serve static files

# ----------------------------------------------------------------------------
# CORS MIDDLEWARE SETUP
# ----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "✅ FastAPI main.py is working correctly"}
