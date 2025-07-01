from together import Together
from config import get_api_key
import logging


logger = logging.getLogger(__name__)
client = Together()  # автоматически берёт ключ из переменной окружения TOGETHER_API_KEY
MAX_RETRIES = 4  # максимальное количество попыток для продолжения

def generate_answer(prompt: str) -> str:
    api_key = get_api_key()
    if not api_key or api_key == "your_api_key_here":
        logger.error("API ключ отсутствует или не задан.")
        return "Ошибка: API ключ не установлен."

    try:
        full_answer = ""
        current_prompt = prompt
        for attempt in range(MAX_RETRIES):
            logger.info(f"[Попытка {attempt + 1}] Отправляем запрос модели...")

            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": current_prompt}],
                max_tokens=500,
                temperature=0.6,
                top_p=0.9,
                top_k=50
            )

            part = response.choices[0].message.content.strip()
            full_answer += part

            if not is_truncated(part):
                break

            current_prompt = f"Продолжи объяснение, начиная с того места, где закончил:\n{full_answer}"

        logger.info("Ответ успешно сгенерирован.")
        return full_answer

    except Exception as e:
        logger.exception("Произошла ошибка при генерации ответа:")
        return f"Произошла ошибка при получении ответа: {str(e)}"

def is_truncated(answer: str) -> bool:
    """Проверяет, возможно ли, что ответ был обрезан."""
    answer = answer.strip()
    if not answer:
        return False
    # Если нет точки в конце, или строка заканчивается многоточием, возможно, ответ обрезан
    return not answer.endswith(('.', '!', '?', '."', '?"')) or answer.endswith('...')


def generate_answer(prompt: str) -> str:
    api_key = get_api_key()
    if not api_key or api_key == "your_api_key_here":
        return "Ошибка: API ключ не установлен."

    try:
        full_answer = ""
        current_prompt = prompt
        for attempt in range(MAX_RETRIES):
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[
                    {"role": "user", "content": current_prompt}
                ],
                max_tokens=500,
                temperature=0.6,
                top_p=0.9,
                top_k=50
            )

            part = response.choices[0].message.content.strip()
            full_answer += part

            if not is_truncated(part):
                break  # Выход, если ответ завершён

            # Подготовка нового запроса — просим продолжить
            current_prompt = f"Продолжи объяснение, начиная с того места, где закончил:\n{full_answer}"

        return full_answer

    except Exception as e:
        return f"Произошла ошибка при получении ответа: {str(e)}"