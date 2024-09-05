from fastapi import FastAPI, Request
import uvicorn
from datetime import datetime
import json
import pytz

app = FastAPI()


def format_timestamp(input_timestamp):
    # Check if the input is an integer (UNIX timestamp)
    if isinstance(input_timestamp, int):
        # Convert UNIX timestamp to a datetime object in UTC
        utc_time = datetime.utcfromtimestamp(input_timestamp)
    
    # Check if the input is a string (ISO format timestamp)
    elif isinstance(input_timestamp, str):
        # Parse the ISO 8601 string into a datetime object
        utc_time = datetime.strptime(input_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    
    else:
        raise ValueError("Invalid input format. Provide either an int or ISO 8601 string.")

    # Format the datetime object to the desired string format
    formatted_time = utc_time.strftime('%d %B %Y - %I:%M %p UTC')

    # Handle special cases for the day (like 1st, 2nd, 3rd, etc.)
    day = utc_time.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    # Return the final formatted string
    return utc_time.strftime(f'{day}{suffix} %B %Y - %I:%M %p UTC')


def convert_timestamp_to_ist(timestamp):
    # Convert timestamp to UTC datetime object
    utc_time = datetime.utcfromtimestamp(timestamp)
    
    # Define IST timezone (UTC+5:30)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Convert UTC time to IST
    ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    
    return ist_time

def convert_iso_to_ist(iso_string):
    # Parse the ISO 8601 string to a datetime object in UTC
    utc_time = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Define IST timezone (UTC+5:30)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Convert UTC time to IST
    ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    
    return ist_time


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
        push_time = format_timestamp(push_time)
        print(f"converted {push_time = }")
        print(push_time)


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
