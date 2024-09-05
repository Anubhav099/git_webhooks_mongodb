from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

class PushObj:
    def __init__(self, author_name, branch, timestamp):
        self.author_name = author_name
        self.branch = branch
        self.timestamp = timestamp
        print(f"PushObj created: {self}")

    def __str__(self):
        return f'"{self.author_name}" pushed to "{self.branch}" on {self.timestamp}'

# 2
@app.post("/")
async def read_root(request: Request):
    if request.headers['Content-Type'] == 'application/json':
        info = await request.json()
        print(f"{info = }")

        branch_name = info['ref'].split('/')[-1]
        push_time = info['repository']['pushed_at']
        if isinstance(push_time, str) and push_time[-1] == 'Z':
            print(f"str {push_time = }")
        elif isinstance(push_time, int):
            print(f"int {push_time = }")

        if 'commits' in info:
            for commit in info['commits']:
                print(f"{commit['author']['name'] = }")
                print(PushObj(commit['author']['name'], branch_name, push_time))
                

        # new_commit_id = info['after'] if 'after' in info else None

        # repo_url = info['repository']['html_url']
        # if 'head_commit' in info:
            # commit_message = info['head_commit']['message']
            # commit_url = info['head_commit']['url']
            # commit_author = info['head_commit']['author']['username']

        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
