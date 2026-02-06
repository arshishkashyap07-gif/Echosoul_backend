
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_routes import router as auth_router
from routes.journal_routes import router as journal_router

app = FastAPI(title="EchoSoul API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(journal_router)

@app.get("/")
def root():
    return {"message": "EchoSoul backend running"}
