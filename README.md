# FastAPI Product Inventory Backend

## 📌 Overview
A backend system built with FastAPI for managing product inventory.

## ⚙️ Features
- CRUD APIs for product management tracking.
- PostgreSQL Database integration using SQLAlchemy
- Input validation with Pydantic
- API testing with Swagger UI


##Create .env in root folder
add your database string
DATABASE_URL=postgresql://username:password@localhost:5432/database_name"

## 🚀 Run Locally

oprn frontend folder:
npm install
npm start

open new/split terminal for running fastapi server
```bash
uvicorn main:app --reload
