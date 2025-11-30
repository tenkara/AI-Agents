# My GIT Repos Summary Agent

## Overview

This agent is designed to summarize the content of my GitHub repositories. It uses a combination of tools to achieve this goal.

## Tools

The agent uses the following tools:

1. `get_github_repos`: This tool fetches the list of repositories from GitHub.
2. `get_repo_content`: This tool fetches the content of a specific repository.
3. `summarize_repo`: This tool summarizes the content of a repository.

## Build Instructions
Create a main.py file
Use MCP to build the MCP AI Agent
Set up the GitHub MCP server either locally or remotely
Generate a GitHub Personal Access Token with appropriate permissions and scope to read all my github repos
Configure the MCP server with the GitHub Personal Access Token

Fetch the list of repos belonging to my github account
Fetch the content of each repo
Summarize the content of each repo
Format and push the summary to a markdown file called my_github_repos_summary.md

## Usage

To use the agent, simply run the following command:

```python
python main.py
```

## Results

The agent will print the summary of each repository to the console.

