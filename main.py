from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()


@app.post("/")
def read_root(request: Request):
    print(f"{request = }")
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        print(info)
        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
