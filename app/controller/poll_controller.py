from typing import List
from fastapi import APIRouter, HTTPException, status
from ..model.poll import PollQuestion, PollQuestionCreate, PollQuestionUpdate, AnswerCreate, AnswerResponse
from ..service import poll_service

router = APIRouter(prefix="/polls", tags=["polls"])


@router.post("/questions", response_model=PollQuestion, status_code=status.HTTP_201_CREATED)
async def create_question(question: PollQuestionCreate):
    return await poll_service.create_question(question)


@router.get("/questions", response_model=List[PollQuestion])
async def get_all_questions():
    return await poll_service.get_all_questions()


@router.get("/questions/{question_id}", response_model=PollQuestion)
async def get_question(question_id: int):
    question = await poll_service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/questions/{question_id}", response_model=PollQuestion)
async def update_question(question_id: int, question: PollQuestionUpdate):
    updated = await poll_service.update_question(question_id, question)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int):
    question = await poll_service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await poll_service.delete_question(question_id)
    return None


@router.post("/questions/{question_id}/answers", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED)
async def submit_answer(question_id: int, answer: AnswerCreate):
    if answer.user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user id")

    # Verify user is registered
    is_registered = await poll_service.is_user_registered(answer.user_id)
    if not is_registered:
        raise HTTPException(
            status_code=403,
            detail="Only registered users can answer poll questions"
        )

    # Check if question exists
    question = await poll_service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        answer_with_question = AnswerCreate(
            user_id=answer.user_id,
            option_choice=answer.option_choice
        )
        return await poll_service.submit_answer(answer_with_question, question_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/answers/{answer_id}", response_model=AnswerResponse)
async def update_answer(answer_id: int, option_choice: str):
    updated = await poll_service.update_answer(answer_id, option_choice)
    if not updated:
        raise HTTPException(status_code=404, detail="Answer not found")
    return updated


@router.get("/questions/{question_id}/summary")
async def get_question_summary(question_id: int):
    question = await poll_service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return await poll_service.get_question_summary(question_id)


@router.get("/users/{user_id}/answers")
async def get_user_answers(user_id: int):
    return await poll_service.get_user_answers(user_id)


@router.get("/users/{user_id}/answer-count")
async def get_user_answer_count(user_id: int):
    return {"user_id": user_id, "total_answers": await poll_service.get_user_answer_count(user_id)}


@router.delete("/users/{user_id}/answers", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_answers(user_id: int):
    await poll_service.delete_user_answers(user_id)
    return None


@router.get("/summary")
async def get_all_questions_summary():
    """Get all questions with their answer summaries and options"""
    return await poll_service.get_all_questions_with_summaries()
