from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()


# 2
@app.post("/")
async def read_root(request: Request):
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(await request.json())
        print(f"{info = }")
        new_commit_id = info['after']
        repo_url = info['respository']['html_url']
        action_time = info['repository']['pushed_at']

        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
