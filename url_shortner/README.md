# URL Shortener API

A simple REST API that converts long URLs into shorter URLs and redirects users to the original destination.

Built using FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- Create shortened URLs
- Redirect short URLs to their original destination
- Prevent duplicate short URLs for the same original URL
- Validate URLs before storing them
- Generate unique short codes
- PostgreSQL database integration
- Database health check endpoint
- Interactive API documentation using Swagger

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn

## Project Structure

```text
url_shortener/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md


````md
# URL Shortener — Setup Guide

This guide explains how to set up and run the **URL Shortener** application locally.

## Prerequisites

Before getting started, make sure you have the following installed:

- Python
- PostgreSQL
- Git

---

## 1. Clone the Repository

Clone the repository and navigate to the project directory:

```bash
git clone <your-github-repository-url>
cd url_shortener
````

---

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

---

### Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Create the PostgreSQL Database

Create a PostgreSQL database named:

```text
url_shortener
```

You can create it using the PostgreSQL command line:

```sql
CREATE DATABASE url_shortener;
```

To verify that the database was created successfully:

```sql
\l
```

---

## 5. Configure Environment Variables

Create a `.env` file in the root directory of the project.

Add the following configuration:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/url_shortener
BASE_URL=http://127.0.0.1:8000
```

Replace the following values with your PostgreSQL credentials:

- `USERNAME` — Your PostgreSQL username
- `PASSWORD` — Your PostgreSQL password

### Example

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/url_shortener
BASE_URL=http://127.0.0.1:8000
```

> **Note:** If your PostgreSQL password contains special characters such as `@`, `#`, `/`, or `:`, make sure to URL-encode them before adding the password to the connection string.

---

## 6. Run the Application

Start the FastAPI application using Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

Once the server starts successfully, the application will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

Access the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Alternative API documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

---

## Setup Complete

Your **URL Shortener API** should now be running locally and ready for development and testing.

---

# API Endpoints

## POST `/shorten`

Creates a shortened URL from the provided original URL.

### Example Request

```json
{
  "url": "https://www.google.com"
}
```

### Example Response

```json
{
  "original_url": "https://www.google.com/",
  "short_url": "http://127.0.0.1:8000/abc123"
}
```

---

## GET `/{short_code}`

Redirects the user to the original URL associated with the provided short code.

### Example Request

```http
GET /abc123
```

The API responds with a redirect to the original URL.

---

## GET `/health`

Checks whether the API is running and verifies the PostgreSQL database connection.

### Example Response

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# Design Decisions

## Duplicate URLs

If the same original URL is submitted more than once, the API returns the existing shortened URL instead of creating duplicate records in the database.

## Short Code Generation

Short codes are generated using Python's `secrets` module with a combination of letters and numbers.

Before storing a generated short code, the application checks whether it already exists in the database. If a collision occurs, a new short code is generated.

## Environment Configuration

Database credentials and the application's base URL are stored using environment variables rather than being hardcoded in the application. This improves security and makes the application easier to configure across different environments.

---

# Testing

The following scenarios were tested:

- Valid URL creation
- Duplicate URL submission
- Invalid URL validation
- Redirect using a valid short code
- Request using a non-existent short code
- PostgreSQL database connectivity

---

# Future Improvements

With additional development time, the following features and improvements could be added:

- Custom short codes
- URL expiration
- Click analytics
- Rate limiting
- Automated tests
- Docker support
- Deployment configuration

---

# Security

## Important Security Check

Make sure your `.env` file is included in `.gitignore` to prevent sensitive information, such as your PostgreSQL credentials, from being pushed to GitHub.

Your `.gitignore` file should include:

```text
venv/
.env
__pycache__/
*.pyc
```

> **Important:** Never commit passwords, database credentials, API keys, or other sensitive configuration values to a public repository.

---

# Author

**Anvith Alva**
