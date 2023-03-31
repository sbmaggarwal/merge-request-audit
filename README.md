# GitLab API Pull Request Data Fetcher

This is a Python script that fetches pull request data from a self-hosted GitLab server using the GitLab API. The script accepts several inputs, including a GitLab API token, server URL, user ID, start time, and end time. It then uses these inputs to fetch all pull requests created by the specified user ID between the given timeframe and count the number of comments each pull request receives. Finally, the script saves all this data in a CSV file with the specified file location.

## Prerequisites

Before running this script, you must have the following:

- A self-hosted GitLab server
- A GitLab API token with read access to the server
- Python 3.7 or higher installed on your system

## How to Run

To run this script, follow these steps:

1. Clone this repository to your local machine.
2. Install the required packages by running the following command in your terminal:
```
pip install python-gitlab
```
3. Open a terminal window and navigate to the directory where the script is located.
4. Run the script using the following command, replacing the placeholders with your own values:
```
python mr_audit.py --token=<your_gitlab_api_token> --url=<your_gitlab_server_url> --user=<user_id> --start=<start_time> --end=<end_time> --file=<file_path>
```

- `token`: Your GitLab API token with read access to the server.
- `url`: The URL of your GitLab server.
- `user`: The ID of the user whose pull requests you want to fetch.
- `start`: The start time of the timeframe in ISO 8601 format (e.g., "2022-01-01T00:00:00Z").
- `end`: The end time of the timeframe in ISO 8601 format.
- `file`: The file path where you want to save the CSV file (e.g., "./data/pull_request_data.csv").

## Output

The script will save the pull request data to a CSV file with the specified file location. The CSV file will contain the following columns:

- Pull Request Link
- Number of Comments
- Pull Request Status
- Pull Request Creation Date
- Pull Request Merged Date

## License

This script is released under the MIT License. See [LICENSE](LICENSE) for more information.