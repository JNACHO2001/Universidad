from fastapi import FastAPI
from routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origenes = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
