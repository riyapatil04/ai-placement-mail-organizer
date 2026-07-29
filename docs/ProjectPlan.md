AI processing will only run for emails that pass duplicate checks and placement-email filters.

## Change in AI Strategy (Gemini → Ollama)

- Original plan: use Gemini API for email summarization and extraction.
- Updated plan: use Ollama to run a local model (Gemma 3 or Phi-3 Mini) for AI tasks.
- Reason:
  - No external API keys.
  - No recurring costs.
  - Data stays on my local machine.
- Impact on roadmap:
  - AI steps now call `ai_service.py` → Ollama instead of Gemini.
  - The prompt aims to return structured JSON with fields:
    `category`, `company`, `role`, `deadline`, `eligibility`, `registration_link`, `summary`.


## End-to-End Processing (V1)

- Scheduler runs every ~10 minutes.
- New emails are fetched from Gmail, deduplicated, and saved as raw records.
- Classification + AI extraction are applied only to likely placement emails.
- AI results are stored in a separate `email_analysis` table.
- If a deadline is found, a Google Calendar event is created automatically.
- The React dashboard displays emails, AI analysis, and calendar events.

## Frontend (V1)

- Single-page React app with:
  - Sidebar (All Emails, Placement, Calendar, Settings).
  - Email list + email details panel.
  - Calendar view showing only extracted deadlines.
  - Search and basic filters (All, Placement, Processed, Unprocessed).
- Dark theme by default, blue accent, clean cards.
- Calls FastAPI for:
  - `GET /emails`, `GET /emails/{id}`, `GET /analysis/{id}`, `GET /calendar`, `POST /sync`.

## React Component Design (V1)

- Main page: `Dashboard`, which owns:
  - `emails`
  - `selectedEmail`
  - `searchText`
  - `filter`
- `Dashboard` calls FastAPI (`GET /emails`) and passes data to:
  - `EmailList` → `EmailCard`
  - `EmailDetails`
  - `Calendar`
- Child components are pure UI that receive props and callbacks.