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

def get_single_updated_gists(username, token, year):
    url = f"https://api.github.com/users/{username}/gists"
    headers = {"Authorization": f"token {token}"}
    params = {"per_page": 100}
    filtered_gists = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch gists: {response.status_code}")
            print(response.json())
            return []

        gists = response.json()
        for gist in gists:
            created_at = datetime.datetime.strptime(gist["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            updated_at = datetime.datetime.strptime(gist["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            
            # Check if the gist was created in the filter year and updated only once
            if created_at.year == year and created_at == updated_at:
                # Get the first file name from the gist
                first_file = list(gist["files"].keys())[0] if gist["files"] else "No files"
                
                filtered_gists.append({
                    "name": first_file,
                    "description": gist["description"] or "No description provided",
                    "url": gist["html_url"],
                    "created_at": created_at,
                })

        # Pagination: Get the next page if available
        url = response.links.get("next", {}).get("url")

    return filtered_gists

def print_items(items, item_type, year):
    if not items:
        print(f"No {item_type} found for {year} with the specified criteria.")
        return

    print(f"\n{item_type} created in {year} with no updates:")
    for item in items:
        print(f"- Name: {item['name']}")
        print(f"  Description: {item['description']}")
        print(f"  URL: {item['url']}")
        print(f"  Created At: {item['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    # Get and print repositories
    repositories = get_single_updated_repositories(github_username, github_token, filter_year)
    print_items(repositories, "Repositories", filter_year)

    # Get and print gists
    gists = get_single_updated_gists(github_username, github_token, filter_year)
    print_items(gists, "Gists", filter_year)