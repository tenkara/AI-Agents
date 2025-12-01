# LinkedIn Resume Updater Agent

An AI agent that fetches your LinkedIn profile data and automatically generates or updates your resume.

## Features

- 🔗 Fetches LinkedIn profile data via API
- 📄 Generates professional resume in multiple formats (Markdown, PDF)
- 🤖 Uses AI to enhance and optimize resume content
- ✨ Customizable templates and styling
- 🔄 Updates existing resume with new information

## Prerequisites

- Python 3.8 or higher
- LinkedIn account
- OpenAI API key (for AI enhancements)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   
   Add to your `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   LINKEDIN_EMAIL=your_linkedin_email
   LINKEDIN_PASSWORD=your_linkedin_password
   ```

## Usage

### Interactive Mode (Jupyter Notebook)
```bash
# Open linkedin-resume-agent.ipynb in VS Code/Jupyter
```

### Command Line
```bash
python main.py
```

## Output

The agent generates:
- `resume.md` - Markdown format resume
- `resume.pdf` - PDF format resume (if weasyprint installed)

## Limitations

- LinkedIn's API access is limited; this uses web scraping as fallback
- Rate limiting may apply
- Some profile sections may require manual input

## Legal Notice

This tool is for personal use only. Respect LinkedIn's Terms of Service and rate limits.
