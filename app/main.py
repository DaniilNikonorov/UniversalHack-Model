from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.endpoints import router as endpoints

app = FastAPI(
    title="University Hack"
)

app.include_router(endpoints)

# Разрешить все источники (для примера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
