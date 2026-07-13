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