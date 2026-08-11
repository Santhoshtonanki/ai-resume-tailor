import os
import re
import sys
from pathlib import Path
from collections import Counter

# Try importing docx, handle gracefully if not installed
try:
    import docx
    from docx import Document
except ImportError:
    print("Error: 'python-docx' library is not installed.")
    print("Please install it using: pip install python-docx")
    sys.exit(1)

# Keyword dictionaries for role classification
ROLE_KEYWORDS = {
    "DevOps": [
        "devops", "ci/cd", "cicd", "kubernetes", "k8s", "docker", "terraform", 
        "ansible", "jenkins", "gitlab", "github actions", "helm", "argocd", 
        "pipeline", "infrastructure as code", "iac", "containerization", "prometheus", "grafana"
    ],
    "Cloud": [
        "cloud", "aws", "azure", "gcp", "ec2", "s3", "iam", "vpc", "serverless", 
        "lambda", "cloudformation", "azure devops", "google cloud", "cloud architect", 
        "cloud engineer", "cloud native", "finops"
    ],
    "Linux": [
        "linux", "rhel", "centos", "ubuntu", "bash", "shell scripting", 
        "system administrator", "sysadmin", "kernel", "redhat", "debian", 
        "system administration", "posix", "cron", "systemd"
    ],
    "NOC": [
        "noc", "network operations center", "monitoring", "nagios", "zabbix", 
        "datadog", "incident management", "ticketing", "servicenow", "routing", 
        "switching", "cisco", "firewall", "network engineer", "network support", 
        "alert response", "sla", "uptime"
    ]
}

RESUME_PATHS = {
    "DevOps": "Global_resumes/Santhosh_DevOps_Global_Resume.docx",
    "Cloud": "Global_resumes/Santhosh_Cloud_Global_Resume.docx",
    "Linux": "Global_resumes/Santhosh_Linux_Global_Resume.docx",
    "NOC": "Global_resumes/Santhosh_NOC_Global_Resume.docx"
}

def analyze_job_description(jd_text):
    """Analyze job description text and score it against role categories."""
    jd_lower = jd_text.lower()
    scores = {}
    matched_words = {}

    for role, keywords in ROLE_KEYWORDS.items():
        score = 0
        matches = []
        for kw in keywords:
            # Count occurrences using regex word boundary or string search
            pattern = r'\b' + re.escape(kw) + r'\b'
            found = len(re.findall(pattern, jd_lower))
            if found > 0:
                score += found
                matches.append(kw)
        scores[role] = score
        matched_words[role] = matches

    # Determine winning role
    best_role = max(scores, key=scores.get)
    max_score = scores[best_role]

    # Fallback to DevOps if no keywords matched
    if max_score == 0:
        best_role = "DevOps"

    return best_role, scores, matched_words

def create_fallback_template(path, role):
    """Creates a placeholder DOCX template if base resume file does not exist."""
    doc = Document()
    doc.add_heading(f"Santhosh - {role} Engineer", 0)
    doc.add_paragraph(f"Email: santhosh@example.com | Phone: +1-234-567-890 | Location: Visakhapatnam, India")
    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(f"Experienced {role} professional with strong skills in automation, infrastructure, and operations.")
    doc.add_heading("Technical Skills", level=1)
    doc.add_paragraph(f"Key Expertise: {role} tools, Scripting, Troubleshooting, CI/CD, Monitoring.")
    doc.add_heading("Work Experience", level=1)
    doc.add_paragraph(f"Senior {role} Specialist — Tech Solutions Inc.
- Managed enterprise systems and automated key pipelines.")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)

def generate_tailored_resume(template_path, output_path, role, matched_keywords):
    """Loads base resume template and saves a tailored copy in generated/."""
    if not os.path.exists(template_path):
        print(f"[*] Base resume template not found at '{template_path}'. Creating sample template...")
        create_fallback_template(template_path, role)

    doc = Document(template_path)
    
    # Save directly into generated folder
    doc.save(output_path)

def generate_cover_letter(role, matched_keywords, output_path):
    """Generates a customized Cover Letter text file."""
    keywords_str = ", ".join(matched_keywords[:6]) if matched_keywords else "cloud infrastructure, automation, and system administration"
    
    cover_letter_text = f"""Dear Hiring Manager,

I am writing to express my enthusiastic interest in the {role} position. With extensive hands-on experience in modern infrastructure management and operational excellence, I am confident in my ability to deliver immediate value to your team.

My technical background aligns directly with your requirements, particularly in areas such as {keywords_str}. Throughout my career, I have focused on building resilient systems, streamlining workflows, and ensuring maximum operational reliability.

Key highlights of my qualifications include:
- Proven expertise in {role} domain practices and tools.
- Hands-on experience with automated deployments, monitoring, and proactive incident response.
- Strong problem-solving skills and a collaborative approach to engineering challenges.

I am excited about the opportunity to contribute to your organization's success and would welcome the chance to discuss how my background matches your team's needs.

Thank you for your time and consideration.

Sincerely,
Santhosh
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cover_letter_text)

def generate_match_report(role, scores, matched_words, output_path):
    """Generates a detailed Match Report text file."""
    report_lines = []
    report_lines.append("=" * 50)
    report_lines.append("           AI RESUME TAILOR - MATCH REPORT          ")
    report_lines.append("=" * 50)
    report_lines.append(f"
[+] Selected Target Role: {role.upper()}")
    report_lines.append("
[+] Category Match Scores:")
    for r, s in scores.items():
        marker = " <--- (Selected)" if r == role else ""
        report_lines.append(f"    - {r:<10}: {s} keyword matches{marker}")

    report_lines.append("
[+] Matched Keywords for Target Role:")
    kw_list = matched_words.get(role, [])
    if kw_list:
        for kw in kw_list:
            report_lines.append(f"    * {kw}")
    else:
        report_lines.append("    * General keyword match (default profile assigned)")

    report_lines.append("
[+] Recommended Resume Template:")
    report_lines.append(f"    {RESUME_PATHS[role]}")
    report_lines.append("
" + "=" * 50)

    report_content = "
".join(report_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

def main():
    print("
==============================================")
    print("      AI RESUME TAILOR - SMART TAILOR         ")
    print("==============================================
")
    print("Paste the Job Description (JD) below.")
    print("When finished, press Enter, then Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) followed by Enter:
")

    try:
        jd_input = sys.stdin.read()
    except KeyboardInterrupt:
        print("
Process interrupted by user.")
        return

    if not jd_input.strip():
        print("[!] Warning: Empty Job Description provided. Proceeding with default DevOps target.")
        jd_input = "DevOps engineer CI/CD Kubernetes Docker AWS"

    # Analyze JD
    role, scores, matched_words = analyze_job_description(jd_input)

    # Ensure output directory exists
    gen_dir = Path("generated")
    gen_dir.mkdir(parents=True, exist_ok=True)

    # File paths
    base_resume_path = RESUME_PATHS[role]
    tailored_resume_path = gen_dir / "Tailored_Resume.docx"
    cover_letter_path = gen_dir / "Cover_Letter.txt"
    match_report_path = gen_dir / "match_report.txt"

    # Generate files
    generate_tailored_resume(base_resume_path, str(tailored_resume_path), role, matched_words[role])
    generate_cover_letter(role, matched_words[role], str(cover_letter_path))
    generate_match_report(role, scores, matched_words, str(match_report_path))

    # Terminal output summary
    print("
" + "=" * 45)
    print("            MATCHING RESULTS                 ")
    print("=" * 45)
    print(f" Selected Role      : {role}")
    print(f" Winning Score     : {scores[role]} keyword hit(s)")
    print(f" Template Selected : {base_resume_path}")
    print("
 Generated Files:")
    print(f"  1. Resume        : {tailored_resume_path.resolve()}")
    print(f"  2. Cover Letter  : {cover_letter_path.resolve()}")
    print(f"  3. Match Report  : {match_report_path.resolve()}")
    print("=" * 45)
    print("
[✓] Resume tailoring process completed successfully!
")

if __name__ == "__main__":
    main()
