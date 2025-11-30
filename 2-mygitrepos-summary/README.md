# GitHub Repository Summary Agent

An AI agent that automatically fetches and summarizes all repositories from a GitHub account using the smolagents framework.

## Features

- Fetches all repositories from a specified GitHub account
- Retrieves repository details including README, file structure, and metadata
- Uses AI to generate comprehensive summaries of each repository
- Outputs a formatted markdown file with all repository summaries

## Prerequisites

- Python 3.8 or higher
- Hugging Face account and API token
- GitHub account (optional: GitHub Personal Access Token for higher rate limits)

## Setup

1. **Create and activate the virtual environment:**

   ```bash
   # The virtual environment should already be created
   # Activate it:
   
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   
   # On Windows (Command Prompt):
   .\venv\Scripts\activate.bat
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Copy `.env.example` to `.env` and fill in your credentials:
   
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   - `HF_TOKEN`: Your Hugging Face API token (get it from https://huggingface.co/settings/tokens)
   - `GITHUB_USERNAME`: Your GitHub username
   - `GITHUB_TOKEN`: (Optional) Your GitHub Personal Access Token for higher API rate limits

## Usage

Run the agent:

```bash
python main.py
```

The agent will:
1. Fetch all repositories from your GitHub account
2. Retrieve content and details for each repository
3. Generate AI-powered summaries
4. Save the results to `my_github_repos_summary.md`

## Tools

The agent uses three custom tools:

1. **get_github_repos**: Fetches the list of repositories from a GitHub account
2. **get_repo_content**: Retrieves detailed content of a specific repository
3. **write_summary_to_file**: Writes the generated summary to a markdown file

## Output

The agent generates a file called `my_github_repos_summary.md` containing:
- Repository name and URL
- Description
- Main programming language
- Stars and forks count
- Key features from README
- File structure overview

## Model

This agent uses the `Qwen/Qwen2.5-Coder-32B-Instruct` model from Hugging Face, which is optimized for code understanding and generation tasks.

## Rate Limits

- **Without GitHub token**: 60 requests per hour
- **With GitHub token**: 5,000 requests per hour

It's recommended to use a GitHub Personal Access Token for better performance.

## Troubleshooting

- **Missing HF_TOKEN**: Make sure you've set your Hugging Face token in the `.env` file
- **Rate limit exceeded**: Add a GitHub Personal Access Token to increase your rate limit
- **Repository not found**: Verify your GitHub username is correct in the `.env` file

