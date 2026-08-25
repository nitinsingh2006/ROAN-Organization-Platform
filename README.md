# ROAN Organization Platform

A comprehensive educational and organization management portal built with **Reflex** (Python). Featuring a cohesive dark glassmorphism design, role-based access control (RBAC), interactive dashboards, PDF generation, and OAuth integration.

---

## 🚀 Features

### 1. Public Marketing Website
* **Branch Showcases:** Dedicated sections for Guitar Academy, Sufiaana Rasoi, Infy X, and Xplore Trails.
* **Responsive Layout:** Mobile-friendly navigation with responsive UI elements.
* **Persistent Forms:** Contact form persistence and styled error/404 pages.

### 2. Multi-Role Portals (RBAC)
* **Student Portal:**
  * View dashboard, enroll or drop courses.
  * Apply for exams and view results.
  * Upload academic documents.
  * Edit student profile and check real-time notifications.
  * Generate and download PDF admit cards and certificates.
* **Faculty Portal:**
  * Student directory access.
  * Track attendance and enter marks/grades.
  * Perform practical evaluations.
* **Institute Portal:**
  * Verify student documents.
  * Update fee status (Paid/Pending).
  * Recommend exam mode (Online/Offline/Hybrid) for forwarded student queues.
* **University Portal:**
  * Approve or reject exam applications.
  * Declare results.
  * Approve or issue course completion certificates.
  * Access university-wide audit trails.
* **Super Admin Portal:**
  * Manage users, view contact messages.
  * Inspect comprehensive system audit logs.
  * View interactive charts and dashboard analytics.
  * Export/Backup database state.

### 3. Core Capabilities
* **Security:** Password hashing, session protection, and server-side role-based routing guards.
* **Authentication:** Traditional email/password sign-in alongside additive **Google** and **GitHub** OAuth options.
* **PDF Engine:** Dynamic PDF generation for certificates and admit cards using ReportLab.
* **Analytics:** Visual data charts for registrations, fee collection pipelines, and application flow.

---

## 🛠️ Tech Stack

* **Frontend & Backend Framework:** [Reflex](https://reflex.dev)
* **Styling:** Tailwind CSS (via Reflex TailwindV4Plugin)
* **PDF Generation:** ReportLab
* **Authentication:** Custom hash-based auth + PyGithub & HTTPX for OAuth callbacks

---

## 📂 Project Structure

```text
ROAN-Organization-Platform/
├── app/
│   ├── components/       # Reusable UI widgets (nav, footer, layout, shell)
│   ├── data/             # Seeding utility and mock DB schemas (seed.py)
│   ├── pages/            # App pages (public marketing and secure portal modules)
│   │   └── portals/      # Role-specific portal views (student, faculty, etc.)
│   ├── states/           # Reflex State classes for state management and logic
│   ├── utils/            # Utilities (PDF generator)
│   └── app.py            # App initialization, config, and routing
├── assets/               # Static files (images, custom CSS, favicon)
├── rxconfig.py           # Reflex configurations
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup & Installation

### Prerequisites
* Python 3.10+ installed.

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nitinsingh2006/ROAN-Organization-Platform.git
   cd ROAN-Organization-Platform
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Reflex:**
   ```bash
   reflex init
   ```

5. **Run the development server:**
   ```bash
   reflex run
   ```
   Open your browser and navigate to `http://localhost:3000`.

---

## 🔑 Demo Credentials

To test the role-based portals out of the box, use the following pre-seeded credentials:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Super Admin** | `admin@roan.edu` | `admin123` |
| **University** | `university@roan.edu` | `university123` |
| **Institute** | `institute@roan.edu` | `institute123` |
| **Faculty** | `faculty@roan.edu` | `faculty123` |
| **Student** | `student@roan.edu` | `student123` |
