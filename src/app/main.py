# ASGI Config for hypercorn
import asyncio

from hypercorn import Config
from hypercorn.asyncio import serve
from app import create_app

config = Config()
config.bind = ["0.0.0.0:8000"]

# Run the application
app = create_app()
asyncio.run(serve(app, config))
