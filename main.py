from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

def PushObj():
    def __init__(self, author_name, branch, commit_message, commit_url, commit_author):
        self.repo_url = repo_url
        self.action_time = action_time
        self.commit_message = commit_message
        self.commit_url = commit_url
        self.commit_author = commit_author

    def __str__(self):
        return f"Repo URL: {self.repo_url}\nAction Time: {self.action_time}\nCommit Message: {self.commit_message}\nCommit URL: {self.commit_url}\nCommit Author: {self.commit_author}"

# 2
@app.post("/")
async def read_root(request: Request):
    if request.headers['Content-Type'] == 'application/json':
        info = await request.json()
        print(f"{info = }")

        for commit in info['commits']:
            commit['author']['name']

        new_commit_id = info['after'] if 'after' in info else None

        repo_url = info['repository']['html_url']
        action_time = info['repository']['pushed_at'] if 'pushed_at' in info['repository'] else None
        if 'head_commit' in info:
            commit_message = info['head_commit']['message']
            commit_url = info['head_commit']['url']
            commit_author = info['head_commit']['author']['username']

        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
