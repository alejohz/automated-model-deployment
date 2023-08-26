from fastapi import FastAPI


app = FastAPI()
# Deployed in glitch
# Url: https://roomy-angry-trapezoid.glitch.me/

@app.get("/")
async def root():
    return {"message": "Hello World"}
