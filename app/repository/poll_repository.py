from .database import database


async def create_question(question_data: dict) -> int:
    query = """
        INSERT INTO poll_questions (title, option_a, option_b, option_c, option_d)
        VALUES (:title, :option_a, :option_b, :option_c, :option_d)
    """
    last_id = await database.execute(query, values=question_data)
    return int(last_id)


async def get_question_by_id(question_id: int):
    query = "SELECT * FROM poll_questions WHERE id = :question_id"
    return await database.fetch_one(query, values={"question_id": question_id})


async def get_all_questions():
    query = "SELECT * FROM poll_questions ORDER BY id"
    return await database.fetch_all(query)


async def update_question(question_id: int, update_data: dict):
    if not update_data:
        return None
    fields = ", ".join(f"{key} = :{key}" for key in update_data)
    query = f"UPDATE poll_questions SET {fields} WHERE id = :question_id"
    values = {**update_data, "question_id": question_id}
    await database.execute(query, values)
    return await get_question_by_id(question_id)


async def delete_question(question_id: int):
    query = "DELETE FROM poll_questions WHERE id = :question_id"
    await database.execute(query, values={"question_id": question_id})


async def save_answer(answer_data: dict) -> int:
    query = """
        INSERT INTO poll_answers (question_id, user_id, option_choice)
        VALUES (:question_id, :user_id, :option_choice)
    """
    last_id = await database.execute(query, values=answer_data)
    return int(last_id)


async def get_answer_by_id(answer_id: int):
    query = "SELECT * FROM poll_answers WHERE id = :answer_id"
    return await database.fetch_one(query, values={"answer_id": answer_id})


async def update_answer(answer_id: int, option_choice: str):
    query = "UPDATE poll_answers SET option_choice = :option_choice WHERE id = :answer_id"
    await database.execute(query, values={"option_choice": option_choice, "answer_id": answer_id})
    return await database.fetch_one("SELECT * FROM poll_answers WHERE id = :answer_id", values={"answer_id": answer_id})


async def get_answers_for_question(question_id: int):
    query = "SELECT * FROM poll_answers WHERE question_id = :question_id"
    return await database.fetch_all(query, values={"question_id": question_id})


async def get_answers_for_user(user_id: int):
    query = "SELECT * FROM poll_answers WHERE user_id = :user_id"
    return await database.fetch_all(query, values={"user_id": user_id})


async def get_answer_count_for_question(question_id: int) -> int:
    query = "SELECT COUNT(*) AS total FROM poll_answers WHERE question_id = :question_id"
    row = await database.fetch_one(query, values={"question_id": question_id})
    return int(row["total"])


async def get_answer_count_for_user(user_id: int) -> int:
    query = "SELECT COUNT(*) AS total FROM poll_answers WHERE user_id = :user_id"
    row = await database.fetch_one(query, values={"user_id": user_id})
    return int(row["total"])


async def delete_user_answers(user_id: int):
    query = "DELETE FROM poll_answers WHERE user_id = :user_id"
    await database.execute(query, values={"user_id": user_id})


async def get_user_answer_for_question(user_id: int, question_id: int):
    """Check if user already answered this question"""
    query = """
        SELECT * FROM poll_answers
        WHERE user_id = :user_id AND question_id = :question_id
    """
    return await database.fetch_one(
        query,
        values={"user_id": user_id, "question_id": question_id}
    )


async def get_all_questions_with_answer_counts():
    """Get all questions with their answer counts per option"""
    query = "SELECT * FROM poll_questions ORDER BY id"
    return await database.fetch_all(query)
