from fastapi import FastAPI
from router import user
import uvicorn
from starlette.responses import RedirectResponse

app = FastAPI()
app.include_router(user.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    except Exception as e:
        print(str(e))