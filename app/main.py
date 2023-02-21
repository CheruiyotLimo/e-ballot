from fastapi import FastAPI



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "The pathway to your internship future."}