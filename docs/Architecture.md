# Architecture – AI Placement Mail Organizer

## 1. Role of the Frontend

- The frontend is a React-based web interface that runs in the browser.
- It shows dashboards, email cards, calendars, and forms for my profile.
- It sends requests to the backend to fetch or update data and displays the responses to the user.

## 2. Role of the Backend

- The backend is a FastAPI server that exposes APIs to the frontend.
- It reads placement emails (via Gmail API), calls AI (Gemini), talks to the database (SQLite), and performs eligibility checks.
- It hides all secrets, credentials, and complex logic from the frontend.

## 3. Why React Should Not Talk Directly to Gmail

- React code runs in the browser, so any Gmail or API keys inside it would be visible to anyone.
- Direct access from the browser to Gmail would create security and permission issues.
- Using the backend as a middle layer lets me control authentication, rate limits, logging, and data validation safely.

## 4. What is an API in This Project?

- An API here is a set of HTTP endpoints exposed by the FastAPI backend.
- Each endpoint defines how the frontend can request data or actions (for example, “get all placement emails” or “save my profile”).
- The API standardizes request and response formats using JSON so React and FastAPI can communicate reliably.

## 5. Difference Between GET and POST (in Our Context)

- GET is used when the frontend wants to **retrieve** data without changing anything, such as fetching a list of processed placement emails.
- POST is used when the frontend wants to **create or send** new data to the backend, such as sending a raw email body to analyze or saving a new user profile.

## 6. Why FastAPI for the Backend

- FastAPI is modern, high-performance, and designed specifically for building APIs with Python. [web:40][web:46]
- It uses Python type hints to automatically generate validation and interactive documentation (OpenAPI/Swagger), which makes testing and debugging easier. [web:37][web:40][web:46]
- Its async support and clean project structure patterns (with `app/main.py`, routers, schemas, services, etc.) make it a good fit for an AI-heavy, API-first backend. [web:37][web:39][web:41][web:44]

## 8. Local AI with Ollama

- The backend uses Ollama to run a local language model (e.g., Gemma 3 or Phi-3 Mini) on my laptop.
- FastAPI never calls an external AI API; instead, it sends prompts to Ollama over `http://localhost:11434`.
- This keeps data on my machine and avoids API keys or monthly AI costs.

## 9. AI Processing Pipeline (High-Level)

- Gmail → `gmail_service` → raw email.
- `email_parser` → extract fields (sender, subject, body, dates, etc.).
- SQLite → store emails and processed status.
- `ai_service` → send only likely placement emails to Ollama and return structured JSON:
  - company, role, deadline, eligibility, registration_link, summary.
- FastAPI → uses the AI result to update the database and later drive the dashboard.

## 10. End-to-End Email Processing Pipeline (V1)

A new email flows through the system as follows:

1. **Scheduler**  
   - Runs every ~10 minutes.  
   - Triggers a check for new emails in Gmail.

2. **Fetch New Emails**  
   - `gmail_service` calls the Gmail API to get recent messages.  
   - Only emails newer than the last sync are considered.

3. **Duplicate Check**  
   - For each email, check if `gmail_message_id` already exists in the `emails` table.  
   - If it exists → skip this email.  
   - If not → continue processing.

4. **Save Raw Email**  
   - Insert the raw email into the `emails` table:  
     - `gmail_message_id`, `thread_id`, `sender`, `subject`, `body`, `received_at`, `is_processed`.

5. **Classify Email**  
   - Call `ai_service` with a short prompt to classify the email:  
     - Categories: `placement`, `college`, `finance`, `shopping`, `travel`, `personal`, `spam`, `other`.

6. **AI Extraction (only for placement emails)**  
   - If `category == "placement"`:  
     - Ask Ollama to extract:  
       - `company`, `role`, `deadline`, `eligibility`, `registration_link`, `summary`.

7. **Save Analysis**  
   - Insert a row into `email_analysis` with:  
     - `email_id` (FK to `emails.id`),  
     - `category`, `company`, `role`, `deadline`, `eligibility`, `registration_link`, `summary`, `processed_at`.

8. **Create Calendar Event (if deadline exists)**  
   - If a valid deadline is found:  
     - Use the Google Calendar API to create an event for the deadline.  
   - If no deadline is found:  
     - Skip this step.

9. **Show on Dashboard**  
   - React frontend calls FastAPI to:  
     - List emails (with or without AI analysis).  
     - Show eligibility, deadlines, and categories.  
   - React never talks directly to Gmail or Ollama.
