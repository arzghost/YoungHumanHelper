import logging
from datetime import datetime
from flask import Flask, render_template, request
import markdown2
from services.answer_generator import build_prompt
from services.llm_service import generate_answer
from config import ensure_env_file
from utils.history import add_to_history, load_history

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)
ensure_env_file()

def log_time(func):
    """Декоратор для замера времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start = datetime.now()
        logging.info(f"Выполняется {func.__name__}...")
        result = func(*args, **kwargs)
        duration = (datetime.now() - start).total_seconds()
        logging.info(f"{func.__name__} завершена за {duration:.2f} сек.")
        return result
    return wrapper

@app.route("/", methods=["GET", "POST"])
def index():
    html_answer = ""
    question = ""
    style = "peer"
    status = ""

    history = load_history()
    # Преобразуем историю в HTML для вывода
    processed_history = []
    for entry in history:
        processed_history.append({
            "timestamp": entry["timestamp"],
            "question": entry["question"],
            "style": entry["style"],
            "answer": entry["answer"],  # исходный текст
            "html_answer": markdown2.markdown(entry["answer"])  # преобразованный
        })

    if request.method == "POST":
        question = request.form["question"].strip()
        style = request.form.get("style", "peer")
        if not question:
            status = "Ошибка: Введите вопрос."
            logging.warning("Пустой вопрос.")
        else:
            logging.info(f"Получен вопрос: '{question}'")
            logging.info(f"Роль: {style}")
            prompt = build_prompt(question, style)

            logging.info("Начинаем генерацию ответа...")
            raw_answer = generate_answer(prompt)
            logging.info("Генерация ответа завершена.")

            html_answer = markdown2.markdown(raw_answer)
            status = "Готово!"
            add_to_history(question, style, raw_answer)  # Сохраняем исходный ответ

    return render_template("index.html",
                           html_answer=html_answer,
                           question=question,
                           style=style,
                           status=status,
                           history=processed_history)


if __name__ == "__main__":
    app.run(debug=True)