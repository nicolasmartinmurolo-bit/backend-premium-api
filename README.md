# Premium Backend API


## 🚀 Description

This project is a production-grade RESTful API built with **FastAPI**, designed following a clean layered architecture (separation of concerns). It implements robust security practices, asynchronous database handling with **PostgreSQL** and **SQLAlchemy**, database migrations with **Alembic**, and **JWT-based stateless authentication**.


## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Database & ORM:** PostgreSQL, SQLAlchemy, Alembic (Migrations)
* **Security & Auth:** Bcrypt (Direct hashing), JSON Web Tokens (JWT)
* **Validation:** Pydantic / Pydantic Settings
* **Containerization & Tools:** Docker, Git / GitHub, Pytest


## 📂 Project Structure

backend-premium-api/
├── app/
│   ├── api/                # API Routers & Endpoints (v1)
│   ├── core/               # Global configuration, database setup & security
│   ├── models/             # SQLAlchemy ORM Database Models
│   └── schemas/            # Pydantic validation schemas
├── alembic/                # Database migration versions
├── tests/                  # Automated tests (Pytest)
├── .env                    # Environment variables (Ignored in Git)
├── requirements.txt        # Project dependencies
└── README.md


## ⚙️ Installation & Running Locally

1. Clone the repository:

git clone [https://github.com/your-username/backend-premium-api.git](https://github.com/your-username/backend-premium-api.git)
cd backend-premium-api


2. Create and activate a virtual environment:

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt
Set up your .env file based on the required configuration (Database URL, Secret Key, etc.).


4. Run the application using Uvicorn:

uvicorn app.main:app --reload


## 📖 API Documentation

Once the server is running, you can access the interactive Swagger UI documentation at:

http://127.0.0.1:8000/docs