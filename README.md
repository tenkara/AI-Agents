# AI-Agents 🤖

A collection of AI-powered agents for automating various tasks including research paper summarization and GitHub repository analysis.

## 📋 Overview

This repository contains multiple AI agent projects that demonstrate different approaches to building intelligent automation tools. Each project uses different frameworks and APIs to accomplish specific tasks.

| Project | Description | Framework | Status |
|---------|-------------|-----------|--------|
| [1-smolagent-summarizer](#1-smolagent-summarizer) | Summarizes Hugging Face daily papers | smolagents + HfApiModel | ✅ Complete |
| [2-mygitrepos-summary](#2-mygitrepos-summary) | Batch GitHub repo summarizer | smolagents + HfApiModel | ✅ Complete |
| [3-mcp-myrepos-summary](#3-mcp-myrepos-summary) | Interactive GitHub repo analyzer | GitHub API + Jupyter | ✅ Complete |

---

## 🔧 Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- API tokens (see individual project requirements)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/tenkara/AI-Agents.git
cd AI-Agents

# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Install base dependencies
pip install python-dotenv requests
```

### Environment Setup

Create a `.env` file in the root directory:

```env
# Required for GitHub API access
GH_TOKEN=your_github_personal_access_token

# Required for Hugging Face projects
HF_TOKEN=your_hugging_face_token

# For project 2
GITHUB_USERNAME=your_github_username
```

---

## 📁 Project Details

### 1-smolagent-summarizer

**Purpose**: Automatically fetches and summarizes the top daily paper from Hugging Face Papers using AI.

#### Features
- 🔍 Scrapes Hugging Face daily papers page
- 📄 Downloads papers from arXiv
- 📖 Reads PDF content (first 3 pages to save tokens)
- 🤖 Uses AI to generate comprehensive summaries

#### Tech Stack
- **Framework**: smolagents (Hugging Face)
- **Model**: Qwen/Qwen2.5-Coder-32B-Instruct via HfApiModel
- **Libraries**: requests, BeautifulSoup, pypdf, arxiv, huggingface_hub

#### Tools Implemented
| Tool | Description |
|------|-------------|
| `get_hugging_face_top_daily_paper()` | Scrapes HF papers page for top daily paper title |
| `get_paper_id_by_title(title)` | Retrieves arXiv paper ID using HF Hub API |
| `download_paper_by_id(paper_id)` | Downloads PDF from arXiv |
| `read_pdf_file(file_path)` | Extracts text from PDF (first 3 pages) |

#### Usage
```bash
cd 1-smolagent-summarizer
pip install smolagents ipywidgets requests beautifulsoup4 pypdf arxiv huggingface_hub
# Open paper-summarizer.ipynb in Jupyter/VS Code and run cells
```

---

### 2-mygitrepos-summary

**Purpose**: AI agent that automatically fetches and generates summaries of all repositories from a GitHub account.

#### Features
- 📦 Fetches all repositories for a specified GitHub user
- 📖 Retrieves README content and file structure
- 🏷️ Extracts metadata (language, stars, forks)
- 📝 Generates comprehensive markdown summary file

#### Tech Stack
- **Framework**: smolagents (Hugging Face)
- **Model**: Qwen/Qwen2.5-Coder-32B-Instruct via HfApiModel
- **Libraries**: requests, python-dotenv

#### Tools Implemented
| Tool | Description |
|------|-------------|
| `get_github_repos(username)` | Fetches list of repos from GitHub API |
| `get_repo_content(username, repo_name)` | Gets README, file structure, metadata |
| `write_summary_to_file(content, filename)` | Writes summary to markdown file |

#### Usage
```bash
cd 2-mygitrepos-summary
pip install -r requirements.txt
python main.py
```

#### Output
Generates `my_github_repos_summary.md` with formatted summaries of all repositories.

---

### 3-mcp-myrepos-summary

**Purpose**: Interactive Jupyter notebook agent for browsing and analyzing GitHub repositories with comprehensive summaries including tech stack, architecture, code functionality, and business analysis.

#### Features
- 📋 Lists all user repositories with metadata table
- 🔍 Interactive repo selection by number
- 💻 Tech stack & language analysis
- 🏗️ Architecture & file structure mapping
- ⚙️ Code module & function extraction
- 💼 Business functionality inference
- 📜 Smart contract analysis (Solidity support)
- 📓 Jupyter notebook analysis

#### Tech Stack
- **Interface**: Jupyter Notebook (VS Code)
- **API**: GitHub REST API (api.github.com)
- **Libraries**: requests, python-dotenv

#### Classes & Methods

**`GitHubClient`** - GitHub API wrapper
| Method | Description |
|--------|-------------|
| `list_user_repos()` | Lists all repos for authenticated user |
| `get_repo_details(owner, repo)` | Gets detailed repo information |
| `get_repo_contents(owner, repo, path)` | Gets directory contents |
| `get_file_content(owner, repo, path)` | Gets decoded file content |
| `get_repo_languages(owner, repo)` | Gets language breakdown |
| `get_repo_tree(owner, repo)` | Gets full file tree |

**`RepoAnalyzer`** - Repository analysis agent
| Method | Description |
|--------|-------------|
| `analyze(owner, repo_name)` | Performs full repository analysis |
| `_get_key_files()` | Reads config files (package.json, requirements.txt, etc.) |
| `_analyze_source_code()` | Extracts functions, classes, routes |
| `_analyze_file_content()` | Parses individual source files |
| `_extract_solidity_info()` | Parses Solidity smart contracts |
| `_analyze_notebook()` | Analyzes Jupyter notebooks |
| `_analyze_business_functionality()` | Infers business domain & features |
| `_detect_frameworks()` | Identifies frameworks from dependencies |
| `print_summary()` | Outputs formatted analysis report |

#### Analysis Output Includes
- **📦 Repository Overview**: Name, description, URL, dates, stars/forks
- **💼 Business Summary**: Domain, core features, user endpoints, integrations, business model
- **💻 Tech Stack**: Languages with percentage bars, detected frameworks
- **🏗️ Architecture**: Directory structure, file counts by type
- **⚙️ Code Modules**: Functions, classes, API routes per file
- **📜 Smart Contracts**: Contract names, inheritance, functions (for Solidity)
- **📖 README Excerpt**: First portion of README content
- **📦 Dependencies**: NPM and Python packages

#### Usage
```bash
cd 3-mcp-myrepos-summary
# Open mcp-myrepos-summary.ipynb in VS Code

# Cell 1: Install packages
# Cell 2: Initialize GitHub client
# Cell 3: List your repositories
# Cell 4: Set SELECTED_REPO_NUMBER = <number>
# Cell 5: Run analysis
```

---

## 📊 Architecture Overview

```
AI-Agents/
├── .env                          # Environment variables (gitignored)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
│
├── 1-smolagent-summarizer/       # Paper summarization agent
│   └── paper-summarizer.ipynb    # Jupyter notebook with tools & agent
│
├── 2-mygitrepos-summary/         # Batch repo summarizer
│   ├── main.py                   # Main agent script
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # Project documentation
│   └── AGENTS.md                 # Agent design notes
│
└── 3-mcp-myrepos-summary/        # Interactive repo analyzer
    └── mcp-myrepos-summary.ipynb # Jupyter notebook with analyzer
```

---

## 🔑 API Tokens Required

| Token | Purpose | Where to Get |
|-------|---------|--------------|
| `GH_TOKEN` | GitHub API access | [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens) |
| `HF_TOKEN` | Hugging Face API | [Hugging Face Settings > Access Tokens](https://huggingface.co/settings/tokens) |

### GitHub Token Permissions
- `repo` - Full control of private repositories (or `public_repo` for public only)
- `read:user` - Read user profile data

---

## 🛠️ Common Issues

### Rate Limiting
GitHub API has rate limits. Using a personal access token increases limits from 60 to 5,000 requests/hour.

### Token Not Found
Ensure `.env` file is in the correct directory and contains valid tokens:
```env
GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

### Import Errors
Install all required packages:
```bash
pip install requests python-dotenv smolagents huggingface_hub
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

**tenkara** - [GitHub Profile](https://github.com/tenkara)
