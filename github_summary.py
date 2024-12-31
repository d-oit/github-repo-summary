import requests
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

github_username = os.getenv("GITHUB_USERNAME")
github_token = os.getenv("GITHUB_TOKEN")
filter_year = int(os.getenv("FILTER_YEAR", 2024))

def get_single_updated_repositories(username, token, year):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    params = {"per_page": 100, "sort": "created"}

    filtered_repos = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch repositories: {response.status_code}")
            print(response.json())
            return []

        repos = response.json()
        for repo in repos:
            created_at = datetime.datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            updated_at = datetime.datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

            # Check if the repo is public, created in the filter year, and updated only once
            if repo["private"] == False and created_at.year == year and created_at == updated_at:
                filtered_repos.append({
                    "name": repo["name"],
                    "description": repo["description"] or "No description provided",
                    "url": repo["html_url"],
                    "created_at": created_at,
                })

        # Pagination: Get the next page if available
        url = response.links.get("next", {}).get("url")

    return filtered_repos

def print_repositories(repos):
    if not repos:
        print(f"No repositories found for {filter_year} with the specified criteria.")
        return

    print(f"\nRepositories created in {filter_year} with no updates:")
    for repo in repos:
        print(f"- Name: {repo['name']}")
        print(f"  Description: {repo['description']}")
        print(f"  URL: {repo['url']}")
        print(f"  Created At: {repo['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    repositories = get_single_updated_repositories(github_username, github_token, filter_year)
    print_repositories(repositories)
