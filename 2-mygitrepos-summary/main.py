"""
GitHub Repository Summary Agent
This agent fetches all repositories from a GitHub account and generates summaries.
"""

import os
import requests
from dotenv import load_dotenv
from smolagents import tool, CodeAgent, HfApiModel

# Load environment variables
load_dotenv()

@tool
def get_github_repos(username: str) -> list:
    """
    Fetch the list of repositories from a GitHub account.
    
    Args:
        username: The GitHub username to fetch repositories for
        
    Returns:
        A list of repository names
    """
    try:
        url = f"https://api.github.com/users/{username}/repos"
        headers = {}
        
        # Use GitHub token if available for higher rate limits
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        repos = response.json()
        repo_list = [{"name": repo["name"], "url": repo["html_url"], "description": repo.get("description", "No description")} for repo in repos]
        
        return repo_list
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching repositories: {e}")
        return []


@tool
def get_repo_content(username: str, repo_name: str) -> str:
    """
    Fetch the content of a specific repository including README and file structure.
    
    Args:
        username: The GitHub username
        repo_name: The name of the repository
        
    Returns:
        A string containing repository information
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        headers = {}
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        # Get repository details
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()
        repo_data = repo_response.json()
        
        # Get README content
        readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
        readme_response = requests.get(readme_url, headers=headers)
        readme_content = ""
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            # Decode base64 content
            import base64
            readme_content = base64.b64decode(readme_data["content"]).decode("utf-8")
        
        # Get repository tree (file structure)
        tree_url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/{repo_data['default_branch']}?recursive=1"
        tree_response = requests.get(tree_url, headers=headers)
        file_structure = []
        if tree_response.status_code == 200:
            tree_data = tree_response.json()
            file_structure = [item["path"] for item in tree_data.get("tree", [])[:50]]  # Limit to first 50 files
        
        content = f"""
Repository: {repo_name}
Description: {repo_data.get('description', 'No description')}
Language: {repo_data.get('language', 'Not specified')}
Stars: {repo_data.get('stargazers_count', 0)}
Forks: {repo_data.get('forks_count', 0)}

README Content:
{readme_content[:2000]}  

File Structure (first 50 files):
{chr(10).join(file_structure)}
"""
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching repository content: {e}")
        return f"Error fetching content for {repo_name}"


@tool
def write_summary_to_file(content: str, filename: str = "my_github_repos_summary.md") -> str:
    """
    Write the summary content to a markdown file.
    
    Args:
        content: The summary content to write
        filename: The name of the file to write to
        
    Returns:
        Success message
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote summary to {filename}"
    except Exception as e:
        return f"Error writing to file: {e}"


def main():
    """Main function to run the GitHub repository summary agent."""
    
    # Get GitHub username from environment or use default
    github_username = os.getenv("GITHUB_USERNAME", "your-github-username")
    
    print(f"Starting GitHub Repository Summary Agent for user: {github_username}")
    
    # Initialize the model
    model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token:
        print("Warning: HF_TOKEN not found in environment variables")
        return
    
    model = HfApiModel(model_id=model_id, token=hf_token)
    
    # Create the agent with our custom tools
    agent = CodeAgent(
        tools=[get_github_repos, get_repo_content, write_summary_to_file],
        model=model,
        add_base_tools=True
    )
    
    # Run the agent with the task
    task = f"""
    Please do the following:
    1. Fetch all repositories for GitHub user '{github_username}'
    2. For each repository, get its content and details
    3. Create a comprehensive summary of all repositories
    4. Write the summary to a file called 'my_github_repos_summary.md' in markdown format
    
    The summary should include for each repository:
    - Repository name and URL
    - Description
    - Main programming language
    - Key features based on README
    - File structure overview
    """
    
    result = agent.run(task)
    print("\n" + "="*50)
    print("Agent execution completed!")
    print("="*50)
    print(result)


if __name__ == "__main__":
    main()

