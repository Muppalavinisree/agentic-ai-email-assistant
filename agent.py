from groq import Groq
import json
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import re

load_dotenv()

# ------------------ CONFIG ------------------
sender_name = os.getenv("SENDER_NAME", "Job Applicant")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RESUME_RULES = [
    ("data scientist", "resumes/RESUME data scientist.pdf"),
    ("data science", "resumes/RESUME data scientist.pdf"),
    ("data analyst", "resumes/RESUME data analyst.pdf"),
    ("software engineer", "resumes/RESUME Soft ware Engineer.pdf"),
    ("machine learning", "resumes/RESUME AI & ML.pdf"),
    ("ai", "resumes/RESUME AI & ML.pdf"),
    ("ml", "resumes/RESUME AI & ML.pdf"),
]


# ------------------ HELPERS ------------------

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


# ------------------ TOOLS ------------------

def send_email(to, subject, body, attachment_path=None):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    if not EMAIL_ADDRESS or not APP_PASSWORD:
        raise ValueError("Email credentials not found in .env file")

    if not is_valid_email(to):
        return {
            "status": "failed",
            "reason": f"Invalid email address: {to}"
        }

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename=file_name
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)

    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "attachment": attachment_path
    }


def retrieve_context():
    with open("docs/agent_rules.txt", "r") as f:
        return f.read()


def extract_json(text):
    if not text:
        raise ValueError("Empty LLM response")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"No JSON found in LLM output:\n{text}")

    json_text = text[start:end + 1]
    return json.loads(json_text)


# ------------------ LLM (GROQ) ------------------

def llm(user_input):
    rules = retrieve_context()

    prompt = f"""
You are an AI agent operating in TOOL MODE.

IMPORTANT ROLE CONSTRAINT:
- You are acting on behalf of the JOB APPLICANT.
- You are NOT a recruiter or company representative.
- You must NEVER claim that positions are available.
- You may ONLY ask about vacancies or respond to recruiter requests.

STRICT RULES (DO NOT BREAK):
- Do NOT ask questions
- Do NOT request clarification
- Do NOT explain anything
- Do NOT include comments
- Do NOT include apologies
- Do NOT include suggestions
- ONLY output valid JSON
- The "to" field MUST be a valid email address.
- Never use placeholders like "HR Email".
- If no email is provided, use the sender's own email address.

TASK:
Convert the user request into a professional email.

SIGNATURE RULE:
- End the email with the name: {sender_name}

OUTPUT FORMAT (JSON ONLY):
{{
  "requires_tool": true,
  "tool": "send_email",
  "arguments": {{
    "to": "email address",
    "subject": "short professional subject",
    "body": "clean professional email body"
  }}
}}

AGENT RULES:
{rules}

USER REQUEST:
"{user_input}"
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)


    content = response.choices[0].message.content.strip()

    return extract_json(content)


# ------------------ EXECUTOR ------------------

def execute_tool(tool, args, user_input):
    attachment_path = None
    text = user_input.lower().replace("\n", " ")

    if "resume" in text or "cv" in text:
        for keyword, path in RESUME_RULES:
            if keyword in text:
                attachment_path = path
                break


    if tool == "send_email":
        return send_email(
            to=args["to"],
            subject=args["subject"],
            body=args["body"],
            attachment_path=attachment_path
        )
    else:
        return {"error": "Unknown tool"}


# ------------------ AGENT LOOP (SAFE) ------------------

goal_completed = False

while not goal_completed:
    user_input = input("Enter your request: ")

    try:
        plan = llm(user_input)
    except Exception as e:
        print("❌ Agent failed to generate a valid plan.")
        print(e)
        continue

    if plan.get("requires_tool"):
        result = execute_tool(plan["tool"], plan["arguments"], user_input)
        print("✅ Tool executed:", result)
        goal_completed = True
    else:
        print("No action required.")
        goal_completed = True
