import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.settings import settings
from app.routes import main_router


def _include_routers(app: FastAPI):
	app.include_router(main_router.router)


def _include_middleware(app: FastAPI):
	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.app.ALLOWED_ORIGINS,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)


def create_app():
	app = FastAPI(title="Posts API")
	_include_routers(app)
	_include_middleware(app)
	return app


if __name__ == "__main__":
	uvicorn.run(
		"app.main:create_app",
		host=settings.app.SERVER_HOST,
		port=settings.app.PORT,
		reload=settings.app.RELOAD,
		factory=True,
	)
