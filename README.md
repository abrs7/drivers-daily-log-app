# Drivers Daily Log App 🚛

Full-stack app (Django + React) for planning truck trips with FMCSA-compliant Hours-of-Service (HOS) tracking and daily log sheet generation.

---

## ✨ Features
- Input trip details (current, pickup, dropoff, cycle hours used).
- Backend (Django + OSRM + custom HOS logic):
  - Computes route, driving time, and required breaks/resets.
  - Generates daily duty logs (on duty, off duty, driving, sleeper).
  - Outputs PNG log sheets filled with duty lines.
- Frontend (React + Vite + Tailwind + shadcn/ui):
  - Form to enter trip details.
  - Map showing route polyline (OpenStreetMap).
  - Table of HOS stops/rests.
  - Gallery of daily log sheets.

---

## 📂 Project Structure
drivers-daily-log-app/
  ├── api/ # Django backend
  │ ├── core/ # urls.py, settings.py
  │ ├── routing/ # route + planner APIs
  │ ├── logs/ # log sheet renderer
  │ └── hos/ # HOS logic
  └── web/ # React frontend
