# React Component Hierarchy and Data Flow (V1)

## 1. Component Tree

```text
App
│
└── Dashboard
    │
    ├── Header
    ├── Sidebar
    ├── SearchBar
    ├── EmailList
    │     └── EmailCard
    ├── EmailDetails
    └── Calendar
```

- `App`: root component, renders the main layout.
- `Dashboard`: main page that owns key state and data.
- `Header`, `Sidebar`: navigation and global UI.
- `SearchBar`: search input for filtering emails.
- `EmailList`: renders a list of `EmailCard` components.
- `EmailCard`: single email preview card.
- `EmailDetails`: detailed view of a selected email + AI analysis.
- `Calendar`: shows extracted deadlines.

## 2. Data Flow (Top → Down)

Data flows from parent to child:

```text
FastAPI
    ↓
Dashboard
    ↓
EmailList
    ↓
EmailCard
```

- `Dashboard` fetches data from FastAPI.
- `Dashboard` passes emails and other props down to:
  - `EmailList`
  - `EmailDetails`
  - `Calendar`
  - `SearchBar` / filters

Child components do **not** fetch data directly from the backend in V1.

## 3. Who Owns the State?

### Emails

- **Owner:** `Dashboard`
- **Reason:**
  - `EmailList` needs the full list.
  - `SearchBar` filters the list.
  - `EmailDetails` shows one email.
  - `Calendar` may show deadlines derived from emails.

If `EmailList` owned the emails, other components would have difficulty accessing them.

### Selected Email

- When a user clicks an `EmailCard` (e.g., “Amazon Internship”):

```text
EmailCard Click
    ↓
Dashboard updates selectedEmail
    ↓
EmailDetails re-renders
```

- `EmailCard` does **not** directly update `EmailDetails`.
- It notifies `Dashboard` (via a callback), and `Dashboard` updates `selectedEmail`.

### State Ownership Summary (V1)

| State          | Owner     | Reason                                           |
|----------------|-----------|--------------------------------------------------|
| `emails`       | Dashboard | Needed by EmailList, SearchBar, Details, Calendar |
| `selectedEmail`| Dashboard | Shared between EmailCard and EmailDetails       |
| `searchText`   | Dashboard | Used to filter emails across the page           |
| `filter`       | Dashboard | Current filter (All, Placement, etc.)           |

## 4. API Calls

In V1, only `Dashboard` (or a dedicated service called by `Dashboard`) should call:

- `GET /emails`

Not `EmailList` or `EmailCard`.

Reasons:

- One API call per load.
- One source of truth for emails.
- Easier to manage loading, errors, and caching.

Later, we can refactor to custom hooks (e.g., `useEmails`) or a global store, but for V1, keeping it in `Dashboard` is simpler and clearer.

## 5. Key Principles

- **Lift State Up:**  
  If multiple components need the same data, keep that data in their closest common parent.

- **Top-down data flow:**  
  Parent components pass data and callbacks down as props.

- **Frontend only talks to FastAPI:**  
  React never calls Gmail or Ollama directly; it only calls FastAPI endpoints.

This design keeps the frontend modular, predictable, and easy to extend.