# Poll Service

A FastAPI microservice for managing poll questions and collecting user responses in the University Poll System.

## Overview

The Poll Service is responsible for:
- Creating and managing poll questions with 4 multiple-choice options
- Storing and updating user poll answers
- Providing poll analytics and result summaries
- Validating that only registered users can answer polls

## Features

- **Full CRUD for Poll Questions**: Create, read, update, and delete poll questions
- **Answer Management**: Submit, update, and retrieve user poll answers
- **Answer Validation**: Ensures each user answers each question only once
- **Analytics**: Get poll results with answer counts per option
- **Inter-Service Communication**: Verifies user registration with the User Service

## Technology Stack

- **Framework**: FastAPI 0.115.0
- **Database**: MySQL 8.0
- **Async Driver**: aiomysql 0.2.0
- **HTTP Client**: httpx 0.27.0
- **Validation**: Pydantic 2.9.2

## Project Structure

```
poll_service/
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Dependencies
├── .env.example                     # Configuration template
├── init.sql                         # Database schema
└── app/
    ├── config.py                    # Configuration settings
    ├── model/
    │   └── poll.py                  # Pydantic models
    ├── controller/
    │   └── poll_controller.py       # REST endpoints
    ├── service/
    │   └── poll_service.py          # Business logic
    └── repository/
        ├── database.py              # Database connection
        └── poll_repository.py       # SQL queries
```

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd poll_system
   ```

2. **Set up environment variables**
   ```bash
   cp poll_service/.env.example .env
   ```

3. **Start MySQL with Docker Compose**
   ```bash
   docker compose up -d
   python init_db.py
   ```

4. **Install dependencies**
   ```bash
   cd poll_service
   pip install -r requirements.txt
   ```

5. **Run the service**
   ```bash
   uvicorn main:app --reload --port 8002
   ```

The service will be available at `http://localhost:8002`

## API Endpoints

### Poll Questions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/polls/questions` | Create a new poll question |
| GET | `/polls/questions` | Get all poll questions |
| GET | `/polls/questions/{question_id}` | Get a specific question |
| PUT | `/polls/questions/{question_id}` | Update a question |
| DELETE | `/polls/questions/{question_id}` | Delete a question |

### Poll Answers

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/polls/questions/{question_id}/answers` | Submit an answer to a question |
| PUT | `/polls/answers/{answer_id}` | Update an existing answer |
| GET | `/polls/users/{user_id}/answers` | Get all answers by a user |
| DELETE | `/polls/users/{user_id}/answers` | Delete all answers by a user |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/polls/questions/{question_id}/summary` | Get answer counts per option |
| GET | `/polls/users/{user_id}/answer-count` | Get total answers submitted by user |
| GET | `/polls/summary` | Get all questions with answer statistics |

## Request/Response Examples

### Create a Poll Question

**Request:**
```bash
POST /polls/questions
Content-Type: application/json

{
  "title": "What is your favorite programming language?",
  "option_a": "Python",
  "option_b": "JavaScript",
  "option_c": "Java",
  "option_d": "Go"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "What is your favorite programming language?",
  "option_a": "Python",
  "option_b": "JavaScript",
  "option_c": "Java",
  "option_d": "Go"
}
```

### Submit an Answer

**Request:**
```bash
POST /polls/questions/1/answers
Content-Type: application/json

{
  "user_id": 5,
  "option_choice": "a"
}
```

**Response:**
```json
{
  "id": 1,
  "question_id": 1,
  "user_id": 5,
  "option_choice": "a"
}
```

### Get Poll Summary

**Request:**
```bash
GET /polls/questions/1/summary
```

**Response:**
```json
{
  "question_id": 1,
  "total_answers": 42,
  "option_a": 15,
  "option_b": 12,
  "option_c": 10,
  "option_d": 5
}
```

## Database Schema

### poll_questions
- `id`: Auto-increment primary key
- `title`: Question text (VARCHAR 255)
- `option_a`, `option_b`, `option_c`, `option_d`: Answer options (VARCHAR 255)

### poll_answers
- `id`: Auto-increment primary key
- `question_id`: Foreign key to poll_questions (ON DELETE CASCADE)
- `user_id`: Reference to user in User Service
- `option_choice`: Selected option (a, b, c, or d)
- **Unique constraint** on (user_id, question_id) to prevent duplicate answers

## Architecture

### MVC Pattern
The service follows the Model-View-Controller architecture:

- **Model** (`poll.py`): Pydantic models for request/response validation
- **Controller** (`poll_controller.py`): HTTP endpoint definitions and routing
- **Service** (`poll_service.py`): Business logic and validation
- **Repository** (`poll_repository.py`): Database query execution

### Inter-Service Communication
The Poll Service communicates with the User Service to:
- Verify user registration status before allowing answers
- Delete user's poll answers when user is deleted from the system

## Running Tests

```bash
# Using Postman or curl
curl http://localhost:8002/polls/questions

# Or use the interactive API docs
http://localhost:8002/docs
```

## Configuration

Edit `.env.example` to customize:

```env
POLL_DB_HOST=localhost
POLL_DB_PORT=3308
POLL_DB_USER=root
POLL_DB_PASSWORD=root_password
POLL_DB_NAME=poll_db
USER_SERVICE_URL=http://localhost:8001
```

## Error Handling

- **400**: Bad request (invalid input)
- **403**: Forbidden (user not registered)
- **404**: Resource not found
- **409**: Conflict (user already answered this question)

## Author

Orian Ben Old

## License

This project is part of the University Poll System backend assignment.
