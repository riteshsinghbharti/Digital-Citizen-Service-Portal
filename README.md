# Digital Citizen Service Portal — E-Governance & Digital Services Platform
Student Name: Ritesh Singh Bharti
Enrollment Number: 25scs1003005661
Program: B.Tech Computer Science & Engineering
Semester: 3rd Semester
Institution: IILM University, Greater Noida, Uttar Pradesh
Internship Organization: YuvaIntern
Internship Role: Junior Web Developer – E-Governance & Digital Services
Internship Duration: 01 August 2026 – 29 August 2026
Duration: 4 Weeks
Mode: Remote
> **B.Tech CSE Internship Project**  
> **Role:** Full-Stack Web Developer – E-Governance Platform  
> **Tech Stack:** Python 3.13, Flask, SQLite with SQLAlchemy ORM, Flask-Login, Flask-WTF, Bootstrap 5.3, HTML5, CSS3, JavaScript

---

## 1. Project Overview
The **Digital Citizen Service Portal** is a production-style, responsive, and accessible e-governance web application designed for citizens to apply for state government certificates and public welfare services online. The portal digitizes application dossiers, supports secure document uploads (Aadhaar, address proof, income slips), provides real-time progress tracking, dispatches status notifications, and enables downloading of digitally signed official certificates upon approval.

The system includes a dedicated administrative management console for nodal officers to review citizen application dossiers, inspect uploaded document scans, update processing stages (`Submitted` → `Under Review` → `Documents Verified` → `Approved` / `Rejected`), resolve citizen grievances, and manage the state service catalog.

---

## 2. Pre-Configured Demo Credentials

| Account Role | Email Address / Login | Password | Access Level & Features |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@gov.in` | `Admin@123` | Nodal Administrative Officer — Executive dashboard, application dossier review, document inspection, status updates, grievance resolution, service catalog CRUD, citizen directory |
| **Citizen (Default)** | `citizen@gmail.com` | `Citizen@123` | Registered Citizen User — Service catalog, multi-step application form, document upload, review & submit, application timeline tracking, alert inbox, printable certificate download, grievance filing |

---

## 3. Technology Stack & Features

- **Backend**: Python 3.13 + Flask framework
- **Database**: SQLite (local zero-configuration database) with `Flask-SQLAlchemy` ORM
- **Authentication & RBAC**: Session-based authentication via `Flask-Login` with `Werkzeug` password hashing (`generate_password_hash` / `check_password_hash`) and role guards (`@admin_required`)
- **Forms & Validation**: `Flask-WTF` forms with automated CSRF protection tokens and multi-step client/server validation
- **File Upload Security**: Local storage validation supporting `.pdf`, `.jpg`, `.jpeg`, and `.png` extensions with a 5 MB file size limit and unique UUID filenames
- **Security Headers**: Middleware response headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`)
- **Frontend & UX**: Responsive layout using Bootstrap 5.3, FontAwesome 6 icons, Google Fonts (Inter), custom status badges, progress timeline steppers, and WCAG accessibility skip links

---

## 4. Directory & Code Base Structure

```text
Digital Citizens Service Portal/
├── app/
│   ├── __init__.py               # Flask app factory, extension init, security headers middleware
│   ├── models.py                 # SQLAlchemy ORM schemas (User, Service, Application, Document, Grievance, Notification)
│   ├── forms.py                  # Flask-WTF validation forms
│   ├── utils.py                  # Secure file upload validator, status badges, timeline helper, admin decorator
│   ├── routes/
│   │   ├── main.py               # Public landing page, services catalog, public tracker, grievance filing, certificate renderer
│   │   ├── auth.py               # Login, registration, and session logout routes
│   │   ├── citizen.py            # Citizen dashboard, multi-step application form, review, timeline detail, notifications, profile
│   │   └── admin.py              # Executive dashboard, dossier review, document inspector, grievance resolver, service catalog CRUD
│   ├── templates/
│   │   ├── base.html             # Master layout with Bootstrap 5, navbar, footer, accessibility skip links
│   │   ├── components/           # Reusable Jinja components (navbar, footer, flash alerts)
│   │   ├── main/                 # Public templates (index, services, track, grievance, printable certificate)
│   │   ├── auth/                 # Login & Registration templates
│   │   ├── citizen/              # Citizen portal templates (dashboard, multi-step apply, review, detail, inbox, profile)
│   │   └── admin/                # Admin console templates (dashboard, application detail, grievances, services CRUD, user list)
│   └── static/
│       ├── css/style.css         # Modern accessible styling, timeline steppers, watermark certificate styling
│       ├── js/main.js            # Client-side form step navigation and interactive helpers
│       └── uploads/documents/    # Secure file storage
├── config.py                     # App configuration (SECRET_KEY, DB URI, MAX_CONTENT_LENGTH)
├── run.py                        # Server entry point
├── seed.py                       # Pre-populated database seeder script
├── requirements.txt              # Dependency specifications
└── README.md                     # Internship documentation and evaluation guide
```

---

## 5. Local Setup & Execution Guide

### Step 1: Requirements
- Python 3.9+ (Python 3.13 tested)
- Pip package manager

### Step 2: Install Dependencies
Open PowerShell or Command Prompt in the project folder and run:
```bash
python -m pip install -r requirements.txt
```

### Step 3: Initialize & Seed Database
Execute the seeder script to populate initial demo accounts and government services:
```bash
python seed.py
```

### Step 4: Run the Application Server
Start the Flask development web server:
```bash
python run.py
```

### Step 5: Open in Web Browser
Navigate to:
```text
http://127.0.0.1:5000
```
Use the quick demo login buttons on the Sign In page or sign in with:
- **Admin**: `admin@gov.in` / `Admin@123`
- **Citizen**: `citizen@gmail.com` / `Citizen@123`

---

## 6. Security Controls & Evaluation Checklist

1. **Password Security**: Passwords are hashed using Werkzeug's secure PBKDF2/SHA256 algorithm before storage in SQLite.
2. **CSRF Protection**: Flask-WTF injects secure session CSRF tokens in all POST forms.
3. **Role-Based Access Control**: Route decorators protect admin routes (`/admin/*`) from unauthorized citizen access. Citizens can only inspect their own application dossiers (`user_id == current_user.id`).
4. **Parameterized Database Queries**: All database interactions use SQLAlchemy ORM parameterized queries, completely neutralizing SQL injection risks.
5. **File Upload Safety**: Uploaded files are validated for allowed file extensions (`.pdf`, `.jpg`, `.jpeg`, `.png`), capped at 5 MB max file size, and saved with randomly generated UUID prefixes.
6. **XSS & Output Escaping**: All user input rendered in templates is escaped automatically via Jinja2.
7. **HTTP Security Headers**: Response headers enforce `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection: 1; mode=block`.
