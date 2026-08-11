from pathlib import Path

content = """Dear Hiring Manager,

I am applying for this opportunity because my experience with Linux, Docker, Jenkins, AWS, and CI/CD aligns well with the role.

I am open to remote opportunities worldwide and willing to relocate for roles that provide visa sponsorship or relocation support.

Thank you for your time.

Regards,
Santhosh Tonanki
"""

Path("generated/Cover_Letter.txt").write_text(content, encoding="utf-8")
print("Saved generated/Cover_Letter.txt")
