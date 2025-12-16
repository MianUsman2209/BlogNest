# BlogNest 🛠️

**BlogNest** is a backend-only personal blog project built using Python.  
It provides core blog functionality such as creating, reading, updating, and deleting articles using **local JSON file storage**, without relying on a database.

This project focuses purely on **backend concepts** and is intended for learning and practice.

---

## 📌 Project Overview

BlogNest implements the backend logic for a personal blog system with two access levels:

### 👥 Guest Access
- View published blog articles
- Read individual articles with publication dates

### 🔐 Admin Access
- Create new blog articles
- Edit existing articles
- Delete articles
- Manage all articles through secured routes

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Framework:** FastAPI  
- **Storage:** Local filesystem (JSON files)  
- **Authentication:** Basic admin authentication  
- **Server:** Uvicorn  

---

## 📂 Data Storage

- Each blog article is stored as a separate **JSON file**
- Article data includes:
  - `title`
  - `content`
  - `published_date`

This flat-file approach avoids database complexity and keeps the project lightweight.

---

## 🚀 API Features

- Create article
- Get all articles
- Get article by ID
- Update article
- Delete article
- Admin-only protected routes

---

## ▶️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/MianUsman2209/BlogNest.git

# Move into project directory
cd BlogNest

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
