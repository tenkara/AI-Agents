"""
LinkedIn Resume Updater Agent
Fetches LinkedIn profile data and generates/updates a professional resume.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class LinkedInClient:
    """Client for fetching LinkedIn profile data."""
    
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.api = None
        self._authenticated = False
    
    def authenticate(self):
        """Authenticate with LinkedIn."""
        try:
            from linkedin_api import Linkedin
            self.api = Linkedin(self.email, self.password)
            self._authenticated = True
            print("✅ LinkedIn authentication successful")
            return True
        except Exception as e:
            print(f"⚠️ LinkedIn API authentication failed: {e}")
            print("📝 You can manually input your profile data instead")
            return False
    
    def get_profile(self, public_id=None):
        """
        Fetch LinkedIn profile data.
        
        Args:
            public_id: LinkedIn public profile ID (from URL)
        
        Returns:
            Profile data dictionary
        """
        if not self._authenticated:
            return None
        
        try:
            if public_id:
                profile = self.api.get_profile(public_id)
            else:
                profile = self.api.get_profile()
            return profile
        except Exception as e:
            print(f"❌ Error fetching profile: {e}")
            return None
    
    def get_profile_contact_info(self, public_id=None):
        """Fetch contact information from profile."""
        if not self._authenticated:
            return None
        
        try:
            contact = self.api.get_profile_contact_info(public_id)
            return contact
        except Exception as e:
            print(f"❌ Error fetching contact info: {e}")
            return None


class ManualProfileInput:
    """Helper class for manual profile data input."""
    
    @staticmethod
    def get_profile_template():
        """Return a template for manual profile input."""
        return {
            "firstName": "",
            "lastName": "",
            "headline": "",
            "summary": "",
            "locationName": "",
            "industryName": "",
            "email": "",
            "phone": "",
            "website": "",
            "experience": [
                {
                    "title": "",
                    "companyName": "",
                    "locationName": "",
                    "description": "",
                    "startDate": {"year": 0, "month": 0},
                    "endDate": {"year": 0, "month": 0},  # Empty for current
                }
            ],
            "education": [
                {
                    "schoolName": "",
                    "degreeName": "",
                    "fieldOfStudy": "",
                    "startDate": {"year": 0},
                    "endDate": {"year": 0},
                    "description": ""
                }
            ],
            "skills": [
                {"name": ""}
            ],
            "certifications": [
                {
                    "name": "",
                    "authority": "",
                    "dateObtained": {"year": 0, "month": 0}
                }
            ],
            "projects": [
                {
                    "title": "",
                    "description": "",
                    "url": ""
                }
            ]
        }
    
    @staticmethod
    def interactive_input():
        """Interactively collect profile data from user."""
        print("\n📝 Manual Profile Input")
        print("=" * 50)
        
        profile = {}
        
        # Basic Info
        print("\n👤 Basic Information:")
        profile["firstName"] = input("First Name: ").strip()
        profile["lastName"] = input("Last Name: ").strip()
        profile["headline"] = input("Professional Headline: ").strip()
        profile["locationName"] = input("Location (City, State/Country): ").strip()
        profile["industryName"] = input("Industry: ").strip()
        profile["email"] = input("Email: ").strip()
        profile["phone"] = input("Phone (optional): ").strip()
        profile["website"] = input("Website/Portfolio URL (optional): ").strip()
        
        print("\n📋 Professional Summary (enter 'done' on new line when finished):")
        summary_lines = []
        while True:
            line = input()
            if line.lower() == 'done':
                break
            summary_lines.append(line)
        profile["summary"] = "\n".join(summary_lines)
        
        # Experience
        profile["experience"] = []
        print("\n💼 Work Experience (enter 'done' to finish adding experiences):")
        while True:
            print(f"\n  Experience #{len(profile['experience']) + 1}:")
            title = input("  Job Title (or 'done'): ").strip()
            if title.lower() == 'done':
                break
            
            exp = {
                "title": title,
                "companyName": input("  Company: ").strip(),
                "locationName": input("  Location: ").strip(),
                "startDate": {
                    "year": int(input("  Start Year: ").strip() or 0),
                    "month": int(input("  Start Month (1-12): ").strip() or 1)
                },
            }
            
            is_current = input("  Current position? (y/n): ").strip().lower() == 'y'
            if not is_current:
                exp["endDate"] = {
                    "year": int(input("  End Year: ").strip() or 0),
                    "month": int(input("  End Month (1-12): ").strip() or 1)
                }
            
            print("  Description (enter 'done' on new line when finished):")
            desc_lines = []
            while True:
                line = input("  ")
                if line.lower() == 'done':
                    break
                desc_lines.append(line)
            exp["description"] = "\n".join(desc_lines)
            
            profile["experience"].append(exp)
        
        # Education
        profile["education"] = []
        print("\n🎓 Education (enter 'done' to finish):")
        while True:
            print(f"\n  Education #{len(profile['education']) + 1}:")
            school = input("  School/University (or 'done'): ").strip()
            if school.lower() == 'done':
                break
            
            edu = {
                "schoolName": school,
                "degreeName": input("  Degree: ").strip(),
                "fieldOfStudy": input("  Field of Study: ").strip(),
                "startDate": {"year": int(input("  Start Year: ").strip() or 0)},
                "endDate": {"year": int(input("  End Year: ").strip() or 0)},
                "description": input("  Description (optional): ").strip()
            }
            profile["education"].append(edu)
        
        # Skills
        print("\n🛠️ Skills (comma-separated):")
        skills_input = input("Skills: ").strip()
        profile["skills"] = [{"name": s.strip()} for s in skills_input.split(",") if s.strip()]
        
        # Certifications
        profile["certifications"] = []
        print("\n📜 Certifications (enter 'done' to finish):")
        while True:
            cert_name = input("  Certification Name (or 'done'): ").strip()
            if cert_name.lower() == 'done':
                break
            
            cert = {
                "name": cert_name,
                "authority": input("  Issuing Authority: ").strip(),
                "dateObtained": {
                    "year": int(input("  Year Obtained: ").strip() or 0),
                    "month": int(input("  Month Obtained (1-12): ").strip() or 1)
                }
            }
            profile["certifications"].append(cert)
        
        return profile


class ResumeGenerator:
    """Generates and formats resumes from profile data."""
    
    def __init__(self, openai_api_key=None):
        self.openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)
    
    def enhance_with_ai(self, text, context="resume bullet point"):
        """Use AI to enhance text for resume."""
        if not self.client:
            return text
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional resume writer. Enhance the following {context} to be more impactful, using action verbs and quantifiable achievements where possible. Keep it concise and professional. Return only the enhanced text, nothing else."
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ AI enhancement failed: {e}")
            return text
    
    def format_date(self, date_dict, include_month=True):
        """Format date dictionary to string."""
        if not date_dict:
            return "Present"
        
        year = date_dict.get("year", 0)
        month = date_dict.get("month", 0)
        
        if not year:
            return "Present"
        
        if include_month and month:
            month_name = datetime(2000, month, 1).strftime("%b")
            return f"{month_name} {year}"
        return str(year)
    
    def generate_markdown(self, profile, enhance=False):
        """
        Generate a markdown resume from profile data.
        
        Args:
            profile: Profile data dictionary
            enhance: Whether to use AI to enhance content
        
        Returns:
            Markdown string
        """
        md = []
        
        # Header
        name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip()
        md.append(f"# {name}\n")
        
        # Contact & Headline
        headline = profile.get("headline", "")
        if headline:
            md.append(f"**{headline}**\n")
        
        contact_parts = []
        if profile.get("email"):
            contact_parts.append(profile["email"])
        if profile.get("phone"):
            contact_parts.append(profile["phone"])
        if profile.get("locationName"):
            contact_parts.append(profile["locationName"])
        if profile.get("website"):
            contact_parts.append(f"[Portfolio]({profile['website']})")
        
        if contact_parts:
            md.append(" | ".join(contact_parts) + "\n")
        
        md.append("---\n")
        
        # Summary
        summary = profile.get("summary", "")
        if summary:
            md.append("## Professional Summary\n")
            if enhance:
                summary = self.enhance_with_ai(summary, "professional summary")
            md.append(f"{summary}\n")
        
        # Experience
        experience = profile.get("experience", [])
        if experience:
            md.append("## Professional Experience\n")
            for exp in experience:
                title = exp.get("title", "")
                company = exp.get("companyName", "")
                location = exp.get("locationName", "")
                start = self.format_date(exp.get("startDate"))
                end = self.format_date(exp.get("endDate"))
                
                md.append(f"### {title}")
                md.append(f"**{company}** | {location} | {start} - {end}\n")
                
                desc = exp.get("description", "")
                if desc:
                    if enhance:
                        desc = self.enhance_with_ai(desc, "job description")
                    # Format as bullet points if not already
                    if not desc.strip().startswith("-") and not desc.strip().startswith("•"):
                        lines = [l.strip() for l in desc.split("\n") if l.strip()]
                        desc = "\n".join([f"- {l}" if not l.startswith("-") else l for l in lines])
                    md.append(f"{desc}\n")
        
        # Education
        education = profile.get("education", [])
        if education:
            md.append("## Education\n")
            for edu in education:
                school = edu.get("schoolName", "")
                degree = edu.get("degreeName", "")
                field = edu.get("fieldOfStudy", "")
                start_year = edu.get("startDate", {}).get("year", "")
                end_year = edu.get("endDate", {}).get("year", "")
                
                degree_str = f"{degree} in {field}" if degree and field else degree or field
                year_str = f"{start_year} - {end_year}" if start_year else str(end_year)
                
                md.append(f"### {school}")
                md.append(f"{degree_str} | {year_str}\n")
                
                if edu.get("description"):
                    md.append(f"{edu['description']}\n")
        
        # Skills
        skills = profile.get("skills", [])
        if skills:
            md.append("## Skills\n")
            skill_names = [s.get("name", "") for s in skills if s.get("name")]
            md.append(", ".join(skill_names) + "\n")
        
        # Certifications
        certifications = profile.get("certifications", [])
        if certifications:
            md.append("## Certifications\n")
            for cert in certifications:
                name = cert.get("name", "")
                authority = cert.get("authority", "")
                date = self.format_date(cert.get("dateObtained"), include_month=False)
                
                if authority:
                    md.append(f"- **{name}** - {authority} ({date})")
                else:
                    md.append(f"- **{name}** ({date})")
            md.append("")
        
        # Projects
        projects = profile.get("projects", [])
        if projects:
            md.append("## Projects\n")
            for proj in projects:
                title = proj.get("title", "")
                desc = proj.get("description", "")
                url = proj.get("url", "")
                
                if url:
                    md.append(f"### [{title}]({url})")
                else:
                    md.append(f"### {title}")
                
                if desc:
                    md.append(f"{desc}\n")
        
        return "\n".join(md)
    
    def save_markdown(self, content, filepath="resume.md"):
        """Save resume to markdown file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Resume saved to {filepath}")
        return filepath
    
    def convert_to_pdf(self, markdown_content, output_path="resume.pdf"):
        """Convert markdown to PDF."""
        try:
            import markdown
            from weasyprint import HTML, CSS
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
            
            # Add styling
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Helvetica Neue', Arial, sans-serif;
                        font-size: 11pt;
                        line-height: 1.5;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 40px;
                    }}
                    h1 {{
                        font-size: 24pt;
                        color: #2c3e50;
                        margin-bottom: 5px;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    h2 {{
                        font-size: 14pt;
                        color: #2c3e50;
                        margin-top: 20px;
                        margin-bottom: 10px;
                        border-bottom: 1px solid #bdc3c7;
                        padding-bottom: 5px;
                    }}
                    h3 {{
                        font-size: 12pt;
                        color: #34495e;
                        margin-bottom: 3px;
                    }}
                    p {{
                        margin: 5px 0;
                    }}
                    ul {{
                        margin: 5px 0;
                        padding-left: 20px;
                    }}
                    li {{
                        margin: 3px 0;
                    }}
                    hr {{
                        border: none;
                        border-top: 1px solid #ecf0f1;
                        margin: 15px 0;
                    }}
                    strong {{
                        color: #2c3e50;
                    }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            HTML(string=styled_html).write_pdf(output_path)
            print(f"✅ PDF resume saved to {output_path}")
            return output_path
        except ImportError:
            print("⚠️ PDF generation requires weasyprint. Install with: pip install weasyprint")
            return None
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            return None


class LinkedInResumeAgent:
    """Main agent that orchestrates LinkedIn data fetching and resume generation."""
    
    def __init__(self):
        self.linkedin = LinkedInClient()
        self.generator = ResumeGenerator()
        self.profile_data = None
    
    def run(self, public_id=None, use_ai=True, output_formats=["md", "pdf"]):
        """
        Run the agent to fetch LinkedIn data and generate resume.
        
        Args:
            public_id: LinkedIn public profile ID (optional)
            use_ai: Whether to use AI to enhance content
            output_formats: List of output formats ("md", "pdf")
        
        Returns:
            Dictionary with generated file paths
        """
        print("\n" + "=" * 60)
        print("🤖 LinkedIn Resume Updater Agent")
        print("=" * 60)
        
        # Try to authenticate with LinkedIn
        print("\n📡 Connecting to LinkedIn...")
        authenticated = self.linkedin.authenticate()
        
        if authenticated:
            # Fetch profile from LinkedIn
            print("\n📥 Fetching profile data...")
            self.profile_data = self.linkedin.get_profile(public_id)
            
            if self.profile_data:
                # Also get contact info
                contact = self.linkedin.get_profile_contact_info(public_id)
                if contact:
                    self.profile_data.update(contact)
        
        # If no LinkedIn data, offer manual input
        if not self.profile_data:
            print("\n⚠️ Could not fetch LinkedIn profile automatically.")
            choice = input("Would you like to:\n  1. Enter profile data manually\n  2. Load from JSON file\n  3. Exit\nChoice (1/2/3): ").strip()
            
            if choice == "1":
                self.profile_data = ManualProfileInput.interactive_input()
            elif choice == "2":
                filepath = input("Enter JSON file path: ").strip()
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        self.profile_data = json.load(f)
                    print(f"✅ Loaded profile from {filepath}")
                except Exception as e:
                    print(f"❌ Error loading file: {e}")
                    return {}
            else:
                print("👋 Exiting...")
                return {}
        
        # Generate resume
        print("\n📝 Generating resume...")
        if use_ai:
            print("   (Using AI enhancement - this may take a moment)")
        
        markdown_content = self.generator.generate_markdown(self.profile_data, enhance=use_ai)
        
        results = {}
        
        # Save outputs
        if "md" in output_formats:
            md_path = self.generator.save_markdown(markdown_content, "resume.md")
            results["markdown"] = md_path
        
        if "pdf" in output_formats:
            pdf_path = self.generator.convert_to_pdf(markdown_content, "resume.pdf")
            if pdf_path:
                results["pdf"] = pdf_path
        
        # Also save profile data as JSON for future updates
        json_path = "profile_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.profile_data, f, indent=2)
        print(f"✅ Profile data saved to {json_path}")
        results["profile_json"] = json_path
        
        print("\n" + "=" * 60)
        print("✅ Resume generation complete!")
        print("=" * 60)
        
        return results
    
    def update_resume(self, json_path="profile_data.json", use_ai=True):
        """
        Update resume from existing profile JSON.
        
        Args:
            json_path: Path to profile JSON file
            use_ai: Whether to use AI enhancement
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.profile_data = json.load(f)
            
            print(f"✅ Loaded profile from {json_path}")
            
            # Regenerate resume
            markdown_content = self.generator.generate_markdown(self.profile_data, enhance=use_ai)
            self.generator.save_markdown(markdown_content, "resume.md")
            self.generator.convert_to_pdf(markdown_content, "resume.pdf")
            
        except Exception as e:
            print(f"❌ Error updating resume: {e}")


def main():
    """Main entry point."""
    agent = LinkedInResumeAgent()
    
    # Check for existing profile data
    if os.path.exists("profile_data.json"):
        choice = input("Found existing profile data. Update existing resume? (y/n): ").strip().lower()
        if choice == 'y':
            agent.update_resume()
            return
    
    # Run full flow
    agent.run(use_ai=True, output_formats=["md", "pdf"])


if __name__ == "__main__":
    main()
