from flask import Flask, request, jsonify
import dbcommands
import json
import os
from typing import Dict, Any, List

# Получаем абсолютный путь к файлу сервера и директорию
server_abs_path = os.path.abspath(__file__)
server_dir_path = os.path.dirname(server_abs_path)

# Создаем Flask приложение
flask_app = Flask(__name__)

# Глобальные переменные для хранения текущего сообщения и ID персонажа
global message
message: str = ''

global char_id
char_id: int = 2

@flask_app.route("/get_message", methods=["GET"])
def show_message() -> jsonify:
    """
    Возвращает текущее сообщение и ID персонажа в формате JSON.
    
    Returns:
        JSON объект с полями:
        - message: текущее сообщение
        - id: ID текущего персонажа
    """
    return jsonify({"message": message, "id": char_id})

@flask_app.route("/send_message", methods=["POST"])
def send_message() -> jsonify:
    """
    Обрабатывает отправку нового сообщения.
    Обновляет глобальные переменные message и char_id,
    сохраняет сообщение в базу данных.
    
    Returns:
        JSON объект с полем code: "success" при успешной обработке
    """
    global message
    message = request.args.get("message")
    global char_id
    char_id = request.args.get("char_id")
    dbcommands.add_message_to_db(message)
    show_message()
    print(char_id)
    return jsonify({"code": "success"})

@flask_app.route("/show_history", methods=["GET"])
def show_history() -> str:
    """
    Возвращает историю сообщений из базы данных.
    
    Returns:
        JSON строка с полем msg, содержащим список сообщений
    """
    history: List[str] = dbcommands.get_history()
    return json.dumps({"msg": history}, ensure_ascii=False)

if __name__ == "__main__":
    # Инициализация базы данных и запуск сервера
    dbcommands.main()
    flask_app.run(debug=True)