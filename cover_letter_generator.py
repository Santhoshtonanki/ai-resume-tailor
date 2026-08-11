job_title = "Platform Engineer"

content = f"""Dear Hiring Manager,

I am applying for the {job_title} role. My experience includes Linux, Docker, Jenkins, AWS, Kubernetes, and CI/CD automation.

I am open to remote opportunities worldwide and willing to relocate for roles that provide visa sponsorship or relocation support.

Regards,
Santhosh Tonanki
"""

with open("Cover_Letter.txt", "w") as f:
    f.write(content)

print("Generated Cover_Letter.txt")
