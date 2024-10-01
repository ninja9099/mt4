from fastapi import FastAPI
from app.routers import mt4

app = FastAPI()

# Include routers
app.include_router(mt4.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)