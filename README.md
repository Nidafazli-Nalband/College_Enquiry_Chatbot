# MMEC College Enquiry Chatbot ✅

**Maratha Mandal Engineering College (MMEC) — Chatbot & Admin Panel**

A Flask-based web application that provides a college-focused chat interface and admin tools. The chatbot answers MMEC-related questions using:
- an offline FAQ (`data/college_info/offline_faq.json`),
- local college files (`info.md`, `class_strengths.json`, `site_pages.json`), and
- an optional AI fallback (OpenAI or Google Gemini) for out-of-scope queries.

---

## 🔍 Project structure (high level)

- `app.py` — main Flask application and API endpoints
- `templates/` — frontend pages and UI (chat UI in `templates/student/chat`)
- `assets/` — images used by the UI (bot avatar, screenshots)
- `data/college_info/` — college content (`offline_faq.json`, `info.md`, `site_pages.json`)
- `data/` — SQLite databases (`users.db`, `mmec.db`) and `settings.json`
- `chat_logs.json` — saved chat logs
- `requirements.txt` — Python package requirements

---

## 🖼️ Assets (gallery)

The repository includes the following images inside `assets/`. Add or replace any file to update screenshots shown in the UI.

- `Admin Dashboard.jpg` — admin dashboard overview
- `Admin Section.jpg` — admin panel screenshot
- `bot.jpeg` — chatbot avatar (recommended)
- `chat.jpg` — chat UI screenshot
- `courses.jpg` — courses page screenshot
- `home page.jpg` — home/splash screenshot
- `login page .jpg` — login page screenshot
- `logo.jpg` — college/project logo
- `photo.jpeg` — sample photo used in UI
- `registeration page.jpg` — registration page screenshot
- `Registered Student.jpg` — registered student view
- `Student dashboard.jpg` — student dashboard screenshot
- `welcome.jpg` — welcome/splash screen

Tip: Use `![alt text](assets/<filename>)` in markdown to render images on GitHub (they display in the repo page).

---

## 🖼️ Gallery preview

<p align="center">
  <img src="assets/bot.jpeg" alt="Bot avatar" width="180" style="margin:8px;" />
  <img src="assets/chat.jpg" alt="Chat UI" width="180" style="margin:8px;" />
  <img src="assets/Admin Dashboard.jpg" alt="Admin Dashboard" width="180" style="margin:8px;" />
  <img src="assets/Student dashboard.jpg" alt="Student Dashboard" width="180" style="margin:8px;" />
</p>

*Tip: add or replace images in the `assets/` folder to update these thumbnails.*

---

## 🧰 Requirements & Installation

Primary packages are in `requirements.txt`:

- Flask>=2.0
- python-dotenv
- openai (optional)
- google-generativeai (optional)
- requests
- beautifulsoup4
- reportlab (optional)
- scikit-learn, joblib (optional for TF-IDF index)

Windows PowerShell (recommended):

```powershell
# create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# upgrade tools and install deps
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

If you won't use external AI features, `openai` and `google-generativeai` can be skipped.

---

## 🔑 Environment variables (optional)

Set API keys and behavior flags via environment variables or a `.env` file:

- `OPENAI_API_KEY` — OpenAI key (optional)
- `GEMINI_API_KEY` — Google Generative key (optional)
- `ALLOW_EXTERNAL_QUERIES` — `1` or `true` to allow external AI calls

Example (PowerShell):

```powershell
$env:OPENAI_API_KEY = 'sk-...'
$env:ALLOW_EXTERNAL_QUERIES = '1'
python app.py
```

---


## ▶️ Run the app (local development)

From project root (inside venv):

```powershell
python app.py
```

- Default host/port: `http://0.0.0.0:5502` (open `http://127.0.0.1:5502/student/chat`)
- On first run the app creates `chat_logs.json`, `data/users.db`, and `data/mmec.db`.
- A default admin is inserted if missing. Change credentials before production.

There are helper scripts in `templates/` such as `run_server.ps1` and `fetch_mmec.py`.

---

## 🧩 How the chatbot prioritizes answers

1. Admin-provided FAQs (persisted in DB)
2. Offline FAQ (`data/college_info/offline_faq.json`) — preferred format: `{ "faqs": [...] }`
3. TF-IDF search results from scraped `site_pages.json` (if `search_index.py` build is present)
4. Optional AI fallback (OpenAI/Gemini) when enabled via env vars

If a query is outside the college scope (e.g., weather, sports), the bot politely refuses and records the question for admin review.

---

## ✏️ Editing college data and FAQs

Primary editable files:

- `data/college_info/offline_faq.json` — add or edit entries under `faqs` for fast matching.
- `data/college_info/info.md` — long-form college description (searchable)
- `data/college_info/class_strengths.json` — structured department/student counts
- `data/college_info/site_pages.json` — pages fetched by scraping (used for TF-IDF search)

After edits, restart the server to pick up changes. To refresh the search index after scraping:

```powershell
python templates/fetch_mmec.py
python -c "import templates.search_index as s; s.build_index()"
```

---

## 🔐 Admin endpoints & management

- `POST /api/admin/reply` — reply to a log entry and persist it to admin FAQs
- `POST /api/admin/delete_student` — permanently delete a student and related data
- `POST /api/admin/toggle_ai` — flips `allow_external_queries` in `data/settings.json`

Admin endpoints require a session token (`X-Session-Token` header or `?token=` query).

---

## Log storage behavior

Saved chat logs are written to `chat_logs.json`. To keep stored logs clean, the server strips AI-disclaimer prefixes and generic "found" messages before saving. This prevents storing lines such as "Note: This answer is not from official MMEC data" or "Found relevant data in ..." in the saved logs.

---

## Static Files and Bot Avatar

Place your bot avatar at `assets/bot.jpeg` (or in `static/` as `bot.jpeg`) so the chat header avatar loads correctly.

If you want the bot avatar shown next to every bot message, I can update `templates/student/chat/chat.js` to include it when rendering messages.

---

## Common Tasks

- Restart server after edits:
```powershell
# stop process (Ctrl+C) then
python app.py
```

- Reset chat logs:
```powershell
Remove-Item .\chat_logs.json; python app.py
```

- Inspect the SQLite DB:
```powershell
# Windows: use sqlite3 if available
sqlite3 data\users.db
.sqlite> .tables
.sqlite> select * from users limit 5;
```

---

## Troubleshooting

- If the chat returns AI fallback errors, ensure `OPENAI_API_KEY` or `GEMINI_API_KEY` are set and `ALLOW_EXTERNAL_QUERIES=1` if you want to allow external AI.
- If images don't load from `/assets`, try copying them to `/static/` and refresh the page to bypass OneDrive/permission issues.

---

If you want, I can also:

- Add bot avatars next to each bot message in the chat history UI.
- Implement a soft-delete mode for students instead of permanent removal.
- Run a quick local test (start server and hit a sample query) and show the result.

---

Happy to continue — tell me which of the optional follow-ups you'd like me to do next.
