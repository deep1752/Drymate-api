from fastapi import FastAPI
from api.main import app  # Your actual FastAPI app

# 👇 Required adapter for Vercel
# Vercel will look for the `handler` variable
# like a serverless function entrypoint
def handler(event, context):
    from mangum import Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
