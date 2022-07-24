from fastapi import FastAPI

import views


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(views.router)
    return app
