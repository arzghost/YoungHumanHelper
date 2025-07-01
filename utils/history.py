import os
import json
from datetime import datetime

HISTORY_FILE = 'history.json'

def ensure_history_file():
    """Создаёт файл истории, если его нет."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"[INFO] Создан файл истории: {HISTORY_FILE}")

def load_history():
    """Загружает историю из файла."""
    ensure_history_file()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_history(history):
    """Сохраняет историю в файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(question, style, answer):
    """Добавляет запись в историю."""
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "style": style,
        "answer": answer
    })
    save_history(history)