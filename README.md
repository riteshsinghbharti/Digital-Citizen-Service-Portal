Here is the complete, single merged `README.md` content in raw Markdown format, ready to be easily copied.

```markdown
# Digital Citizen Service Portal — E-Governance & Digital Services Platform

An end-to-end, production-style, responsive e-governance web application developed as part of a B.Tech Computer Science & Engineering internship project. The platform digitizes state government service delivery, application dossier workflows, document verification, and official certificate issuance.

```

---

## 🏛️ Internship & Student Metadata

Here is the student and internship metadata organized cleanly in Markdown table format:

| Parameter | Details |
| --- | --- |
| **Student Name** | Ritesh Singh Bharti |
| **Enrollment Number** | 25scs1003005661 |
| **Academic Program** | B.Tech in Computer Science & Engineering |
| **Semester** | 3rd Semester |
| **Academic Institution** | IILM University, Greater Noida, Uttar Pradesh, India |
| **Internship Organization** | YuvaIntern |
| **Internship Role** | Junior Web Developer – E-Governance & Digital Services |
| **Internship Period** | 01 August 2026 – 29 August 2026 (4 Weeks) |

---

##  About the Institutions

### About IILM University

**IILM University, Greater Noida**, is a premier institution dedicated to offering practical, industry-oriented technical education. The Department of Computer Science & Engineering emphasizes hands-on software development, system design, security, and project-based learning to solve real-world problems.

### About YuvaIntern

**YuvaIntern** is a career-focused internship platform providing students with practical exposure to software engineering, full-stack web development, and digital service design through structured assignments, code reviews, and industry-oriented project frameworks.

---

##  Project Overview & Problem Statement

### Problem Statement

Traditional paper-based government service delivery often suffers from physical queue bottlenecks, manual tracking inefficiencies, lack of application status transparency, potential document loss, and delayed certificate distribution for citizens living in remote or rural regions.

### Proposed Solution

The **Digital Citizen Service Portal** provides an accessible digital public infrastructure platform where citizens can discover state government schemes, submit multi-step application dossiers online, upload supporting identity and income documents securely, track processing stages in real time, and download digitally signed certificates upon approval.

### Primary Objectives

* **Digitize Service Delivery**: Eliminate physical paperwork for public certificate applications.
* **Ensure System Security**: Enforce robust authentication, Role-Based Access Control (RBAC), CSRF mitigation, and secure document upload validation.
* **Provide Process Transparency**: Offer an interactive progress timeline stepper for real-time tracking.
* **Deliver Nodal Governance Tools**: Supply an administrative console for dossier verification, status management, grievance resolution, and service catalog management.

---

##  Key System Features

### Citizen Portal Features

* **Authentication & Profile Management**: Secure registration, login session handling, and profile overview.
* **Government Service Catalog**: Categorized repository of public schemes and certificate services.
* **Multi-Step Application Form**: Guided application submission with step navigation.
* **Secure Document Upload**: Application dossier attachments (Identity, Address, Income proofs).
* **Application Dossier Review**: Self-service verification prior to final submission.
* **Real-Time Tracking & Timeline**: Visual status progression stepper (`Submitted` → `Approved`/`Rejected`).
* **In-App Notifications**: Status alert notifications delivered directly to the citizen inbox.
* **Printable Certificate Download**: Digital certificate generation with verification metadata for approved applications.
* **Public Grievance Redressal**: Submission portal for public feedback and application inquiries.

### Administrator Features

* **Nodal Executive Dashboard**: Real-time aggregate metrics on applications, processing queues, and grievances.
* **Dossier Review & Document Inspector**: Detailed dossier verification interface with secure viewer for uploaded scans.
* **Lifecycle Management**: Stage-by-stage application progression updates (`Submitted` → `Under Review` → `Documents Verified` → `Approved`/`Rejected`).
* **Service Catalog CRUD**: Administrative interface to create, update, or deactivate public service schemes.
* **Grievance Resolution Console**: Management interface to review, respond to, and resolve citizen grievances.
* **Citizen Directory**: Central database view for administrative reference.

---

##  Application Lifecycle Workflow

```text
       ┌────────────────┐
       │   Submitted    │  <-- Citizen completes dossier & uploads documents
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │  Under Review  │  <-- Nodal officer opens dossier for inspection
       └───────┬────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Documents Verified  │  <-- Attachments inspected & validated
    └──────────┬───────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│   Approved   │ │   Rejected   │  <-- Decision finalized by Nodal Officer
└──────┬───────┘ └──────────────┘
       │
       ▼
┌───────────────────────────┐
│ Certificate Downloadable  │  <-- Citizen prints official document
└───────────────────────────┘

```

---

##  Technology Stack

```text
+-----------------------------------------------------------------------+
|                            FRONTEND LAYER                             |
|       HTML5  •  CSS3  •  JavaScript (ES6)  •  Bootstrap 5.3           |
|         FontAwesome 6 Icons  •  Google Fonts (Inter)                  |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                            BACKEND LAYER                              |
|              Python 3.13  •  Flask Microframework                     |
| Flask-Login (Sessions) • Flask-WTF (Forms/CSRF) • Werkzeug (Security) |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                            DATABASE LAYER                             |
|                 SQLite3  •  Flask-SQLAlchemy ORM                      |
+-----------------------------------------------------------------------+

```

| Domain | Technology / Library | Specification / Purpose |
| --- | --- | --- |
| **Language** | Python 3.13 | Core backend runtime execution environment |
| **Framework** | Flask | Lightweight microframework and WSGI app architecture |
| **Database** | SQLite3 | Local persistent database engine |
| **ORM** | Flask-SQLAlchemy | Database abstraction layer and parameterized query engine |
| **Authentication** | Flask-Login | User session lifecycle and login state management |
| **Security Hashing** | Werkzeug | Secure PBKDF2/SHA256 password hashing |
| **Form Management** | Flask-WTF / WTForms | Server-side form validation and CSRF token injection |
| **User Interface** | Bootstrap 5.3 | Responsive grid system, utilities, and components |
| **Development Tools** | Visual Studio Code, Git, GitHub, pip | IDE environment, version control, dependency management, and repository hosting |

---

##  Security Architecture & Controls

The portal implements strict defensive security mechanisms:

1. **Cryptographic Password Storage**: Plaintext passwords are never stored. Passwords are hashed using Werkzeug's secure implementation (`generate_password_hash` / `check_password_hash`) before persistence.
2. **CSRF Token Injection**: Flask-WTF injects secure, session-bound CSRF tokens into all state-changing HTTP POST requests.
3. **Role-Based Access Control (RBAC)**: Custom routing decorators (`@admin_required`) protect administrative endpoints (`/admin/*`) from unauthorized citizen access.
4. **Data Isolation**: Citizens are restricted via database filters (`user_id == current_user.id`) to access only their own application dossiers.
5. **SQL Injection Neutralization**: All database interactions are managed via SQLAlchemy ORM parameterized queries, preventing SQL injection vulnerabilities.
6. **Secure File Upload Pipeline**:
* Extension whitelist restricted strictly to `.pdf`, `.jpg`, `.jpeg`, and `.png`.
* File payload execution safeguards enforced via `MAX_CONTENT_LENGTH = 5 * 1024 * 1024` (5 MB cap).
* Filenames are replaced with cryptographically unique UUIDs prior to local disk write operations to prevent path traversal.


7. **Automated Output Encoding**: Jinja2 auto-escaping is active across all templates to prevent Cross-Site Scripting (XSS).
8. **HTTP Defense Headers**: Custom middleware injects standard security headers into every response:
* `X-Content-Type-Options: nosniff`
* `X-Frame-Options: SAMEORIGIN`
* `X-XSS-Protection: 1; mode=block`
* `Referrer-Policy: strict-origin-when-cross-origin`



---

##  Project Structure

```text
Digital Citizen Service Portal/
│
├── app/
│   ├── __init__.py         # App factory, extension bindings, security header middleware
│   ├── models.py           # Database models (User, Service, Application, Document, Grievance, Notification)
│   ├── forms.py            # Flask-WTF forms and validation logic
│   ├── utils.py            # Secure upload validator, status badges, timeline helper, admin decorator
│   ├── routes/
│   │   ├── main.py         # Landing, public services catalog, tracking, grievances, certificate renderer
│   │   ├── auth.py         # Authentication (Login, Logout, Register)
│   │   ├── citizen.py      # Citizen dashboard, application filing, review, inbox, profile
│   │   └── admin.py        # Executive dashboard, dossier review, CRUD, grievance resolver
│   ├── templates/
│   │   ├── base.html       # Master layout template with Bootstrap 5 & accessibility skip links
│   │   ├── components/     # Reusable UI partials (Navbar, Footer, Flash alerts)
│   │   ├── main/           # Public pages (Index, Services, Tracker, Grievance, Certificate)
│   │   ├── auth/           # Login and Registration views
│   │   ├── citizen/        # Citizen views (Dashboard, Form, Review, Timeline, Inbox, Profile)
│   │   └── admin/          # Admin views (Dashboard, Application Detail, Grievances, Service CRUD, User List)
│   └── static/
│       ├── css/style.css   # Custom layout styles, timeline steppers, watermark certificate styling
│       ├── js/main.js      # Client-side form step navigation and dynamic UI helpers
│       └── uploads/        # Directory for secure file storage
│
├── docs/                   # Additional project documentation
├── instance/               # SQLite runtime database container
├── config.py               # Central configuration settings (SECRET_KEY, DB URI, MAX_CONTENT_LENGTH)
├── run.py                  # Web application entry point script
├── seed.py                 # Seed script for demo database population
├── requirements.txt        # Python dependency manifest
├── prompt.txt              # Specification reference prompt
└── README.md               # Internship documentation and repository guide

```

---

##  Internship Weekly Progress Log

### Week 1: Brand Identity, Architecture & Style Guide

* Analyzed e-governance requirements and public service application workflows.
* Defined application architecture, database schemas, and data relationships.
* Designed visual identity, color scheme, typography system, and accessible UI guidelines.

### Week 2: Responsive Prototype & Layout Design

* Implemented responsive interface layouts using Bootstrap 5.3 and Jinja2 templating.
* Developed wireframes and page layouts for citizen and admin flows.
* Implemented UI/UX enhancements and multi-step client/server form validation navigation.

### Week 3: Quality Assurance, Testing & Workflow Logic

* Built administrative dossier review, document inspection, and status management features.
* Implemented defensive security controls (CSRF protection, file upload security, RBAC guards).
* Conducted systematic functional testing, bug identification, and workflow logic validation.

### Week 4: Performance, Accessibility & Security Audit

* Executed functional end-to-end user testing across citizen and administrator roles.
* Conducted comprehensive performance, accessibility (WCAG skip links), and security audits.
* Finalized repository artifacts, weekly progress reports, and academic documentation.

---

##  Learning Outcomes & Competencies

### Technical Competencies

* **Backend Architecture**: Mastering modular Flask applications using the Application Factory pattern and Blueprint routes.
* **ORM & Data Modeling**: Designing database schemas with foreign key relationships, model properties, and parameterized queries using SQLAlchemy.
* **Security Controls**: Implementation of secure authentication pipelines, role-based authorization, defensive upload handling, and HTTP security headers.
* **Frontend & UX Engineering**: Crafting mobile-responsive, accessible web interfaces utilizing modern Bootstrap 5.3, custom CSS steppers, and client-side JavaScript.
* **Tooling & Version Control**: Utilizing VS Code, Git, GitHub, and Python pip package management for modern web software workflows.

### Professional Skills

* **Systems Analysis**: Translating real-world e-governance workflows into functional software modules.
* **Software Quality Assurance**: Conducting systematic testing, bug identification, form validation checks, and security verification.
* **Technical Documentation & Project Planning**: Authoring structured technical documentation, time management, and managing software development lifecycles.

---

##  Internship Documentation

All official documentation files, progress reports, and design layouts are organized within the repository:

* 📁 [Internship Documents](https://www.google.com/search?q=./Internship%2520Document/) — Contains official offer letter and completion certificate.
* 📁 [Weekly Progress & Audit Reports](https://www.google.com/search?q=./Internship%2520Report%2520Files/) — Includes weekly logs (Weeks 1–3) and the Week 4 comprehensive audit report.
* 📁 [Web Application Wireframe Layouts](https://www.google.com/search?q=./Web%2520Application%2520Layout/) — PDF exports detailing interface layouts and UI designs (`internship_web_application01.pdf` through `04.pdf`).

---

##  Installation & Setup Guide

Follow these instructions to run the application locally.

### Step 1: Clone the Repository

```bash
git clone [https://github.com/riteshsinghbharti/Digital-Citizen-Service-Portal.git](https://github.com/riteshsinghbharti/Digital-Citizen-Service-Portal.git)
cd Digital-Citizen-Service-Portal

```

### Step 2: Install Dependencies

Ensure Python 3.9+ (Python 3.13 tested) is installed. Install required packages using `pip`:

```bash
python -m pip install -r requirements.txt

```

### Step 3: Initialize and Seed Database

Run the seeder script to initialize the SQLite database and populate baseline demo accounts and public services:

```bash
python seed.py

```

### Step 4: Launch Development Server

```bash
python run.py

```

### Step 5: Access Application

Open your web browser and navigate to:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

##  Demonstration Credentials

> ** DEMONSTRATION NOTICE:** The credentials listed below are configured **exclusively for local evaluation, testing, and academic assessment**. They must not be utilized in production environments.

| Role | Email Address / Login | Password | Access Level & Features |
| --- | --- | --- | --- |
| **Administrator** | `admin@gov.in` | `Admin@123` | Nodal Administrative Officer — Executive dashboard, application dossier review, document inspection, status updates, grievance resolution, service catalog CRUD, citizen directory. |
| **Citizen (Default)** | `citizen@gmail.com` | `Citizen@123` | Registered Citizen User — Service catalog, multi-step application form, document upload, review & submit, application timeline tracking, alert inbox, printable certificate download, grievance filing. |

---

## 🏛️ Academic Submission & Declaration

This project is submitted in fulfillment of the B.Tech Computer Science & Engineering 3rd Semester Internship requirement at **IILM University, Greater Noida**.

### Declaration

I hereby declare that the work presented in this repository is an authentic record of my internship project completed under the guidance provided by **YuvaIntern** and evaluated by the Department of Computer Science & Engineering, IILM University.

---

*Developed as a B.Tech Computer Science & Engineering internship project at IILM University, Greater Noida, during my internship with YuvaIntern.*

**Author:**

**Ritesh Singh Bharti**

B.Tech Computer Science & Engineering

IILM University, Greater Noida, Uttar Pradesh, India

GitHub: [riteshsinghbharti](https://www.google.com/search?q=https://github.com/riteshsinghbharti)

```

```
