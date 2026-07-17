from typing import List, Optional
import httpx
from ..model.poll import PollQuestion, PollQuestionCreate, PollQuestionUpdate, AnswerCreate, AnswerResponse
from ..repository import poll_repository
from ..config import config


async def create_question(question_data: PollQuestionCreate) -> PollQuestion:
    question_id = await poll_repository.create_question(question_data.model_dump())
    return await get_question(question_id)


async def get_question(question_id: int) -> Optional[PollQuestion]:
    row = await poll_repository.get_question_by_id(question_id)
    if not row:
        return None
    return PollQuestion(**row)


async def get_all_questions() -> List[PollQuestion]:
    rows = await poll_repository.get_all_questions()
    return [PollQuestion(**row) for row in rows]


async def update_question(question_id: int, question_data: PollQuestionUpdate) -> Optional[PollQuestion]:
    update_payload = {k: v for k, v in question_data.model_dump().items() if v is not None}
    if not update_payload:
        return await get_question(question_id)
    updated = await poll_repository.update_question(question_id, update_payload)
    if not updated:
        return None
    return PollQuestion(**updated)


async def delete_question(question_id: int) -> None:
    await poll_repository.delete_question(question_id)


async def is_user_registered(user_id: int) -> bool:
    """Verify user is registered in the system"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{config.USER_SERVICE_URL}/users/{user_id}"
            )
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get("is_registered", False)
            return False
    except Exception:
        return False


async def submit_answer(answer_data: AnswerCreate, question_id: int) -> AnswerResponse:
    # Check if user already answered this question
    existing_answer = await poll_repository.get_user_answer_for_question(
        answer_data.user_id, question_id
    )
    if existing_answer:
        raise ValueError(f"User {answer_data.user_id} has already answered question {question_id}")

    answer_payload = answer_data.model_dump()
    answer_payload["question_id"] = question_id
    answer_id = await poll_repository.save_answer(answer_payload)
    row = await poll_repository.get_answer_by_id(answer_id)
    return AnswerResponse(**row)


async def update_answer(answer_id: int, option_choice: str) -> Optional[AnswerResponse]:
    updated = await poll_repository.update_answer(answer_id, option_choice)
    if not updated:
        return None
    return AnswerResponse(**updated)


async def get_question_summary(question_id: int):
    answers = await poll_repository.get_answers_for_question(question_id)
    # Count responses per option to show poll results
    return {
        "question_id": question_id,
        "total_answers": len(answers),
        "option_a": sum(1 for row in answers if row["option_choice"] == "a"),
        "option_b": sum(1 for row in answers if row["option_choice"] == "b"),
        "option_c": sum(1 for row in answers if row["option_choice"] == "c"),
        "option_d": sum(1 for row in answers if row["option_choice"] == "d"),
    }


async def get_user_answers(user_id: int):
    answers = await poll_repository.get_answers_for_user(user_id)
    return answers


async def get_user_answer_count(user_id: int) -> int:
    return await poll_repository.get_answer_count_for_user(user_id)


async def delete_user_answers(user_id: int) -> None:
    await poll_repository.delete_user_answers(user_id)


async def get_all_questions_with_summaries():
    """Get all questions with their answer summaries"""
    questions = await poll_repository.get_all_questions_with_answer_counts()
    result = []

    for question in questions:
        summary = await get_question_summary(question["id"])
        question_data = {
            "id": question["id"],
            "title": question["title"],
            "option_a": question["option_a"],
            "option_b": question["option_b"],
            "option_c": question["option_c"],
            "option_d": question["option_d"],
            "summary": summary
        }
        result.append(question_data)

    return result
