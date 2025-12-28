# Agentic AI – Automated Email Assistant

An **agentic AI-based email automation system** that converts natural language and incoming email context into autonomous, rule-governed actions.  
The system uses a **cloud-based LLM (Groq)** combined with **Retrieval-Augmented Generation (RAG)** and a deterministic executor to draft and send professional emails securely.

---

## 🔹 Overview

This project demonstrates a real-world **agentic AI workflow** where reasoning, retrieval, and execution are clearly separated.  
The agent is designed to act as a **job applicant**, intelligently responding to emails based on predefined rules while ensuring safety, professionalism, and correctness.

---

## 🛠️ Tech Stack

- **Python**
- **Groq Cloud LLM**
- **Retrieval-Augmented Generation (RAG)**
- Prompt Engineering
- SMTP (Email Automation)
- JSON-based Tool Execution
- Environment Variables (`.env`)

---

## 🧠 System Architecture

1. Incoming email or user request is analyzed for intent  
2. Relevant context is retrieved using **RAG** (resumes, templates, rules)  
3. **Groq-hosted LLM** reasons over intent and retrieved context  
4. Structured JSON output is generated  
5. Executor validates rules and triggers SMTP if allowed  

This ensures **controlled autonomy** instead of unrestricted AI behavior.

---

## 🤖 Agentic Rules for Email Agent

The agent strictly follows the rules below before taking any action:

1. If an incoming email explicitly asks for a **resume**, the agent must send the **relevant resume as an attachment**.  
2. Resume selection must be **based on the role mentioned** in the email.  
3. If an email asks for **confirmation before sending documents**, reply politely **without attaching files**.  
4. If an email requests **additional documents**, attach **all requested documents** in the response.  
5. If an email is **informational** or does not request any action, **no reply should be sent**.  
6. All email responses must be **professional, polite**, and written from the **perspective of a job applicant**.

These rules are enforced at the **executor level**, ensuring deterministic behavior.

---

## 🔍 Retrieval-Augmented Generation (RAG)

- RAG retrieves **resumes, templates, and contextual rules** before response generation.  
- Retrieved context is injected into the LLM prompt at **inference time**, reducing hallucinations.  
- The agent prioritizes **retrieved knowledge over model assumptions**.  
- The retrieval layer is modular and extensible.

---

## 🔐 Security Practices

- Email credentials are stored securely using **environment variables**  
- No secrets are hardcoded in the codebase  
- `.env` files are excluded from version control  

---
## 📂 Project Structure
agentic-ai-email-assistant/
├── agent.py
├── docs/
├── .gitignore
├── .env.example
└── README.md

---

## 🚀 Usage
Run the agent and provide an email or natural language request.  
The system autonomously decides whether to respond, attach documents, or take no action—based on agentic rules.

---<img width="382" height="99" alt="image" src="https://github.com/user-attachments/assets/a8ec2555-88cf-4073-ac53-8336905919b9" />
![WhatsApp Image 2025-12-28 at 22 40 42](https://github.com/user-attachments/assets/b20b2f21-6d55-452e-b47f-98e787e7109a)
<img width="384" height="96" alt="image" src="https://github.com/user-attachments/assets/8cc83d4d-5988-4c82-8493-995cb6c3e3f4" />
![WhatsApp Image 2025-12-28 at 22 41 47](https://github.com/user-attachments/assets/28fd16b2-4fae-48cb-8889-496b61c5f99e)



## 👤 Author
**Vinisree Muppala**  
Aspiring Software Engineer | Full Stack & Applied AI

---

## 📜 License
This project is for educational and demonstration purposes.
