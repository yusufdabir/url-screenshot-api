
🔍 URL Screenshot & Tracker API

This project is a simple Flask-based web app that allows users to:

✅ Submit any website URL  
✅ Automatically take full-page scrolling screenshots using Selenium  
✅ Track screenshot generation progress using Job ID  
✅ View all screenshots after completion  
✅ (Optional) Get completion notification via webhook

---

📸 Features

- 🔗 Input any valid website URL
- 🧠 Background thread takes screenshots with scrolling
- 🆔 Unique Job ID assigned to each submission
- 🖼️ View screenshots on `/results/<job_id>` page
- 🔁 Page auto-refreshes until screenshots are ready
- 🔔 Optional webhook callback with screenshot links
- 🛠️ Status check API: `/status/<job_id>`
- 📁 All screenshots served from `/screenshots/<filename>`

---

🚀 How It Works

1. User enters a URL (e.g., https://example.com)
2. Selenium launches headless Firefox, scrolls & takes screenshots
3. Each screenshot is saved in the `screenshots/` folder with unique names
4. A Job ID is generated to track status
5. After completion, screenshots are visible at `/results/<job_id>`
6. If webhook is provided, a JSON payload is POSTed to it

---

🧪 Example Webhook Payload

{
  "job_id": "abc123",
  "status": "completed",
  "screenshots": [
    "http://localhost:5000/screenshots/ss_abc123_0.png",
    "http://localhost:5000/screenshots/ss_abc123_1.png"
  ]
}

---

🛠️ Requirements

- Python 3.10+
- Flask
- Selenium
- geckodriver.exe (for Firefox)
- Firefox browser installed

Install dependencies:
pip install -r requirements.txt

---

▶️ Run the App

python app.py

Then visit: http://localhost:5000

---

📂 Folder Structure

screenshot_api/
│
├── app.py
├── job_store.py
├── requirements.txt
├── screenshots/            # All screenshots saved here
├── templates/
│   ├── home.html           # URL input form
│   └── results.html        # Show screenshots

---

🔐 Notes

- Webhook URL is optional
- No login/authentication required
- Temporary job storage (dictionary) — no database used
- Auto-refresh in results page using meta tag

---

👨‍💻 Developer

Made with ❤️ by Mohammad Yusuf Dabir 

