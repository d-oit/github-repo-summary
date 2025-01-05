# GitHub Repository and Gist Filter Script

This Python script filters and lists public GitHub repositories that:
- Were **created** in a specified year.
- Have been updated only once (i.e., the `created_at` and `updated_at` timestamps are the same).

The script uses the GitHub API to fetch and display repository details, such as:
- Repository name
- Description
- URL
- Creation date

## Features
- Filters repositories by:
  - Creation year.
  - Update count (only shows repos with no updates after creation).
  - Visibility (only public repositories).
- Displays repository details in a user-friendly format.
- Utilizes environment variables for secure configuration.

## Prerequisites

### 1. Python Installation
Make sure you have Python 3.7+ installed. You can download it from the [official Python website](https://www.python.org/downloads/).

### 2. Required Python Packages
Install the required Python modules using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. GitHub Personal Access Token
Generate a personal access token from your GitHub account with the following scopes:
- `public_repo` (to access public repositories).

## Setup

### 1. Clone the Repository
Clone this repository to your local machine.

### 2. Create a `.env` File
Create a `.env` file in the root directory and add the following:
```
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
FILTER_YEAR=2024
```
Replace `your_github_username` and `your_github_personal_access_token` with your actual GitHub username and token.

### 3. Exclude Sensitive Files
Ensure your `.env` file is excluded from version control by adding it to `.gitignore`:
```
.env
```

## Usage
Run the script using Python:
```bash
python github_summary.py
```

## Running Tests
Run the tests using `pytest`:
```bash
pytest
```
The script will output a list of repositories matching the criteria, including their name, description, URL, and creation date.

## Example Output
```
Repositories created in 2024 with no updates:
- Name: example-repo
  Description: An example repository
  URL: https://github.com/your_username/example-repo
  Created At: 2024-01-15 10:23:45
```

## Notes
- The script supports pagination for users with many repositories.
- If no repositories match the criteria, it will display a relevant message.

## License
This project is licensed under the MIT License.
