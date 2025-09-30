# Feature Voting System

Deliverables:
- Backend API: FastAPI + SQLite
- Web UI: Angular
- Native Mobile UI: iOS (SwiftUI)
- Loom walkthrough: https://www.loom.com/share/aa34cae60d72447583f2bb97ba2e3f0e?sid=3f6d1ab7-e0e9-4dcd-8d60-df688ee6f583
- Prompts log: see `prompts.txt`

## Run Guide (summary)
- Backend: see `/backend` README section
- Web (Angular): see `/web` README section
- iOS: open `/ios` project in Xcode and run on Simulator

---
###Feature Voting System

A full-stack mini-app.
Users can propose new features and upvote others.

## Project Structure
```bash
Exercise-JCR/
├── backend/                  # FastAPI + SQLite backend API
│   ├── main.py               # API routes: list, create, upvote
│   ├── models.py             # SQLAlchemy models
│   └── requirements.txt
├── web/feature-voting-web/   # Angular frontend
│   ├── src/app/components/   # FeatureCreate + FeatureList
│   ├── src/app/services/     # Angular service calling backend
│   └── src/environments/     # API_BASE set to localhost:8000
└── ios/FeatureVoting/        # iOS SwiftUI app
    ├── ContentView.swift     # Displays list + upvote
    ├── API.swift             # Networking with backend
    └── Feature.swift         # Model
```
---

##⚙️ How to Run
Backend (FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
---


#Endpoints:
GET /features
POST /features
POST /features/{id}/upvote
GET /health
---

###Frontend (Angular)
cd web/feature-voting-web
npm install
ng serve --port 4200

Visit: http://localhost:4200

Ensure backend is running at http://localhost:8000

---

###Mobile (iOS SwiftUI)

Open ios/FeatureVoting.xcodeproj in Xcode.

Select a simulator (e.g., iPhone 15).

Run ▶️ to build.

App loads from http://127.0.0.1:8000.
---

📦 Requirements

Python 3.10+
Node.js 18+ / npm
Angular CLI

Xcode 15+ (for iOS simulator)
---

##📝 Notes

The project is intentionally minimal but functional: UI is plain, logic is complete.
API_BASE is configured for localhost:8000; update if deploying remotely.
