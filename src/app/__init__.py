__version__ = "2024.01.01"

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware


def create_app() -> FastAPI:
    """Function to create FastAPI application.
        Returns:
            FastAPI: FastAPI application.
    """
    app = FastAPI()
    # Mount all middlewares.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    return app
