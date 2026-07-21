# Poll Service

Service for managing poll questions and collecting answers from registered users.

## How to Run

```bash
# Start Docker and database
docker compose up -d
python init_db.py

# Run the service
cd poll_service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

Access at: http://localhost:8002/docs

## What It Does

- Create and manage poll questions with 4 options (a, b, c, d)
- Let registered users submit answers
- Store and update user responses
- Show poll results and analytics

## API Endpoints

**Questions:**
- `POST /polls/questions` - Create question
- `GET /polls/questions` - Get all questions
- `GET /polls/questions/{id}` - Get specific question
- `PUT /polls/questions/{id}` - Update question
- `DELETE /polls/questions/{id}` - Delete question

**Answers:**
- `POST /polls/questions/{id}/answers` - Submit answer
- `PUT /polls/answers/{id}` - Update answer
- `GET /polls/users/{user_id}/answers` - Get user answers
- `DELETE /polls/users/{user_id}/answers` - Delete user answers

**Analytics:**
- `GET /polls/questions/{id}/summary` - Get question results
- `GET /polls/users/{user_id}/answer-count` - Count user answers
- `GET /polls/summary` - All questions with results

## Database

Two tables:
- `poll_questions` - question text and options
- `poll_answers` - user answers with unique constraint on (user_id, question_id)

## Configuration

Copy `.env.example` and edit:
- `POLL_DB_HOST=localhost`
- `POLL_DB_PORT=3308`
- `USER_SERVICE_URL=http://localhost:8001` (for user verification)
