from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()


# 2
@app.post("/")
async def read_root(request: Request):
    if request.headers['Content-Type'] == 'application/json':
        info = await request.json()
        print(f"{info = }")
        new_commit_id = info['after']
        repo_url = info['respository']['html_url']
        action_time = info['repository']['pushed_at']
        if 'head_commit' in info:
            commit_message = info['head_commit']['message']
            commit_url = info['head_commit']['url']
            commit_author = info['head_commit']['author']['username']

        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
