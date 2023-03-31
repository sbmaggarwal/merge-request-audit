import requests
import csv
import datetime
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("gitlab_api.log"),
        logging.StreamHandler()
    ]
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Fetch pull request data from GitLab API.")
parser.add_argument("file_path", type=str, help="File path to save CSV file")
parser.add_argument("api_token", type=str, help="GitLab API token")
parser.add_argument("server_url", type=str, help="GitLab server URL")
parser.add_argument("user_id", type=int, help="User ID to filter pull requests")
parser.add_argument("start_time", type=str, help="Start time in ISO format")
parser.add_argument("end_time", type=str, help="End time in ISO format")
args = parser.parse_args()

# GitLab API token and server URL
api_token = args.api_token
server_url = args.server_url

# User ID, start time, and end time
user_id = args.user_id
start_time = args.start_time
end_time = args.end_time

# File path to save CSV file
file_path = args.file_path

# GitLab API endpoint
endpoint = f"{server_url}/api/v4/projects/<project ID>/merge_requests"

# Set headers for GitLab API request
headers = {"Private-Token": api_token}

# Set query parameters for GitLab API request
params = {
    "created_after": start_time,
    "created_before": end_time,
    "author_id": user_id,
    "state": "all",
    "per_page": 100,
    "page": 1,
}

# Send GitLab API request to fetch merge requests
merge_requests = []
while True:
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        merge_requests.extend(data)
        if not response.links.get("next"):
            break
        params["page"] += 1
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching merge requests: {e}")
        raise SystemExit(e)

# Extract required data from each merge request and save to CSV file
with open(file_path, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        [
            "Pull Request Link",
            "Number of Comments",
            "Pull Request Status",
            "Pull Request Creation Date",
            "Pull Request Merged Date",
        ]
    )
    for merge_request in merge_requests:
        comments_endpoint = f"{endpoint}/{merge_request['iid']}/discussions"
        comments_response = requests.get(comments_endpoint, headers=headers)
        comments_data = comments_response.json()
        num_comments = sum([len(d["notes"]) for d in comments_data])
        creation_date = datetime.datetime.strptime(
            merge_request["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        creation_date_str = creation_date.strftime("%m/%d/%Y %H:%M:%S")
        merged_date_str = ""
        if merge_request.get("merged_at"):
            merged_date = datetime.datetime.strptime(
                merge_request["merged_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            merged_date_str = merged_date.strftime("%m/%d/%Y %H:%M:%S")
        writer.writerow(
            [
                merge_request["web_url"],
                num_comments,
                merge_request["state"],
                creation_date_str,
                merged_date_str,
            ]
        )
        logging.info(f"Data saved to CSV file: {file_path}")