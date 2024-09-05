from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime
import json
import pytz

app = FastAPI()


def format_timestamp(input_timestamp):
    if isinstance(input_timestamp, int):
        utc_time = datetime.utcfromtimestamp(input_timestamp)
    elif isinstance(input_timestamp, str):
        utc_time = datetime.strptime(input_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    else:
        return f"{input_timestamp}"

    formatted_time = utc_time.strftime('%d %B %Y - %I:%M %p UTC')
    day = utc_time.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    return utc_time.strftime(f'{day}{suffix} %B %Y - %I:%M %p UTC')


# 2
@app.post("/")
async def read_root(request: Request):
    if request.headers['Content-Type'] == 'application/json':
        info = await request.json()
        print(f"\n{info = }\n\n")

        if 'pull_request' in info: # 'pull_request' event
            """
                Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
                Sample: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
            """
            author_name = info['pull_request']['user']['login']
            from_branch = info['pull_request']['head']['ref']
            to_branch = info['pull_request']['base']['ref']
            action_time = info['pull_request']['created_at']

            print(f'"{author_name}" submitted a pull request from "{from_branch}" to "{to_branch}" on {action_time}')
        else: # 'push' event
            """
                Format: {author} pushed to {to_branch} on {timestamp}
                Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
            """
            branch_name = info['ref'].split('/')[-1]
            push_time = format_timestamp(info['repository']['pushed_at'])

            for commit in info['commits']:
                print(f'"{commit["author"]["name"]}" pushed to "{branch_name}" on {push_time}')
                
        return info


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
