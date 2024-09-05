from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()


# 2
@app.post("/")
def read_root(request: Request):
    print(f"{request = }")
    print(f"{request.method = }")
    print(f"{request.headers = }")
    print(f"{request.headers['x-github-delivery']} = ")
    print(f"{request.headers['x-github-event']} = ")
    print(f"{request.headers['x-github-hook-installation-target-type'] = }")
    print(f"#{request.body() = }")
    print(f"#{request.body = }")
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json())
        print(info)
        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
