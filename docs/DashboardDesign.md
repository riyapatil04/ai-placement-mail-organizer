# Dashboard UI and API Requirements (V1)

## 1. Main Layout

```text
+------------------------------------------------------+
| Header                                               |
+----------+-------------------------------------------+
| Sidebar  | Email List          | Email Details       |
|          |                     |                     |
|          |                     |                     |
+----------+---------------------+---------------------+
```

- **Header**: app name, small user/profile info, sync button.
- **Sidebar**: navigation between sections.
- **Email List**: list of email cards (paginated or scrollable).
- **Email Details**: detailed view of one email + AI analysis.

## 2. Sidebar (Navigation)

**V1 sections:**

- 📥 All Emails
- 🎓 Placement
- 📅 Calendar
- ⚙️ Settings

**Future sections (for later):**

- 💰 Finance
- ✈️ Travel
- 🛒 Shopping
- 📄 Bills

Each sidebar item will navigate to a different route/view.

## 3. Email List

Each email card shows (at minimum):

- Company (if available, otherwise sender)
- Role / subject line
- Relative time (e.g., “2 hours ago”)
- Tag or badge: “Placement”, “Deadline Found”, etc.

Example card:

> **Amazon**  
> SDE Internship  
> 2 hours ago  
> ✅ Deadline Found

Clicking a card opens the **Email Details** view.

## 4. Email Details

For a selected email, show:

- Subject
- Sender
- Date
- Full email body (or a readable view)
- AI Summary
- Extracted fields:
  - Company
  - Role
  - Eligibility
  - Deadline
  - Registration Link (as clickable)

If no AI analysis exists, show a placeholder like “No AI analysis available yet”.

## 5. Calendar View

Instead of integrating Gmail’s calendar UI, show only **extracted deadlines**.

Example:

> **August**
> - 15  Amazon Registration
> - 18  Microsoft OA
> - 22  Adobe Deadline

Clicking a calendar entry opens the related email (the one that had that deadline).

## 6. Search and Filters

**Search by:**

- Company
- Subject
- Sender

**V1 filters:**

- All
- Placement
- Processed (has AI analysis)
- Unprocessed (no AI analysis yet)

Later we can add filters by category (finance, travel, etc.).

## 7. Theme

Recommended V1 theme:

- 🌙 Dark mode by default
- Clean white/gray cards on dark background
- Blue accent color for primary actions
- Simple, professional, minimal design

## 8. Required Backend APIs

Frontend will only call FastAPI endpoints; it never touches Gmail or Ollama directly.

| API               | Purpose                                 |
|-------------------|------------------------------------------|
| `GET /emails`     | List emails (with optional filters)      |
| `GET /emails/{id}`| Get details of one email                 |
| `GET /analysis/{id}` | Get AI analysis for an email          |
| `GET /calendar`   | Get list of extracted deadlines/events   |
| `POST /sync`      | Trigger manual Gmail sync (optional)     |

Additional endpoints (e.g., search, filters) can be added later, but this is the core set for V1.

## 9. Key Design Principles

- **UI is not your database.**  
  Frontend only knows: “I need a list of emails”, “I need deadlines”.  
  It does not care if data came from Gmail, SQLite, or AI.

- **Backend responsibility:**  
  - Talk to Gmail
  - Run AI
  - Store data
  - Expose clean JSON APIs

- **Frontend responsibility:**  
  - Call FastAPI
  - Display data
  - Handle user interactions

This keeps the system modular and easy to extend later.