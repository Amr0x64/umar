from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from openai import OpenAI
import json

app = Flask(__name__)

class QuizParser:
    def __init__(self, json_data):
        self.questions = self.parse_json(json_data)
    
    def parse_json(self, json_data):
        """Парсит JSON строку в список объектов вопросов"""
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return []
    
    def get_questions(self):
        """Возвращает список всех вопросов"""
        return self.questions
    
    def get_question_by_index(self, index):
        """Возвращает вопрос по индексу"""
        try:
            return self.questions[index]
        except IndexError:
            return None

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def send_gpt(search):
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-chat:free",
    messages=[
        {
        "role": "user",
        "content": f"{search}"
        }
    ]
    )
    return completion.choices[0].message.content
theme = "похожих на что где когда"
promt = """дай мне 10 вопросов высокой сложности на тему похожих на что где когда , вопрос должен выводиться в формате json ключ это вопрос, 
а значение это ответ, то есть вида [{"question": "",  "answer": "", "incorrect": []},  и тд ]. Не выводи ничего кроме json вопроса.
 В incorrect будет два элемента в массиве , два неверных ответа, но потенциально могли бы быть правильными. Не надо дополнять ответ форматирование. Не используй / в ответах"""

# answer = send_gpt(promt)

# print(answer)
# Создаем парсер
parser = QuizParser("""
    [
  {
    "question": "В каком году был основан город Санкт-Петербург?",
    "answer": "1703",
    "incorrect": ["1700", "1712"]
  },
  {
    "question": "Какой химический элемент обозначается символом 'Au'?",
    "answer": "Золото",
    "incorrect": ["Аргон", "Алюминий"]
  },
  {
    "question": "Кто написал роман 'Война и мир'?",
    "answer": "Лев Толстой",
    "incorrect": ["Фёдор Достоевский", "Иван Тургенев"]
  },
  {
    "question": "Какая самая длинная река в мире?",
    "answer": "Нил",
    "incorrect": ["Амазонка", "Янцзы"]
  },
  {
    "question": "Как называется самая высокая гора в мире?",
    "answer": "Эверест",
    "incorrect": ["Килиманджаро", "Аконкагуа"]
  },
  {
    "question": "Какой язык программирования был создан первым?",
    "answer": "Фортран",
    "incorrect": ["Кобол", "Алгол"]
  },
  {
    "question": "Кто открыл закон всемирного тяготения?",
    "answer": "Исаак Ньютон",
    "incorrect": ["Галилео Галилей", "Альберт Эйнштейн"]
  },
  {
    "question": "Как называется самая большая пустыня в мире?",
    "answer": "Сахара",
    "incorrect": ["Гоби", "Антарктическая пустыня"]
  },
  {
    "question": "В каком году человек впервые полетел в космос?",
    "answer": "1961",
    "incorrect": ["1957", "1969"]
  },
  {
    "question": "Какой художник написал картину 'Мона Лиза'?",
    "answer": "Леонардо да Винчи",
    "incorrect": ["Микеланджело", "Рафаэль"]
  }
]
""")
# parser = QuizParser(answer)
# Получаем конкретный вопрос
# first_question = parser.get_question_by_index(0)
# print("\nПервый вопрос:", first_question)
# print("\nПервый вопрос:", first_question["answer"])


# Переменная с текстом
question = ""
game_data = {}
game_count = 0
players = defaultdict(int)

i = 0

@app.route('/')
def home():
    """Главная страница с кнопкой присоединения к игре"""
    return render_template('start.html')

@app.route('/start_game', methods=['GET'])
def start_game():
    """Обработчик входа в игру"""
    global players
    # Получаем IP пользователя
    # Добавляем в словарь с начальным значением 0
    name = request.args.get('name')
    print(name)
    if players[name] != 0:

        players[name] = players[name]
    else:
        players[name] = 0
    
    response = make_response(redirect(url_for('get_quiz_def')))
    
    # Устанавливаем куки с именем игрока
    response.set_cookie(
        'name', 
        name,
        max_age=60*60*24*7,  # Срок жизни 7 дней
        httponly=True,       # Защита от XSS
    )
    
    return response


@app.route('/quiz-label', methods=['GET'])
def get_quiz_def():
    """Quiz игра основная страницав"""
    return render_template('index.html', question=question)


def change_quiestion():
    """апи для получения вопроса и овтета"""
    global i
    global question
    global players_submit 

    if len(parser.get_questions()) > i:
        set_question = parser.get_question_by_index(i)
        print(set_question["question"] + "апи")
        question = set_question
        print("смена вопроса")
        players_submit = 0
        i += 1

@app.route('/question', methods=['GET'])
def get_question():
    """апи для получения вопроса"""
    global question

    return jsonify(question)


@app.route('/init-game', methods=['GET', 'POST'])
def get_start_game():
    """Старт игры для админа"""
    if request.method == "POST":
        change_quiestion()
        return render_template("admin_start.html")
    else:
        return render_template("admin_start.html")

players_submit = 0

"""проврить правильность"""
@app.route('/check-answer/<answer>', methods=['GET'])
def check(answer):
    global players_submit
    global players
    global question

    players_submit += 1
    name = request.cookies.get('name')  
    
    print("сравнение" + question["answer"] + " " + answer)
    if question["answer"] == answer:
        if players_submit == len(players):
            change_quiestion()

        players[name] = players[name] + 1
        return jsonify("""{"status": "ok"}""")
    else:
        if players_submit == len(players):
            change_quiestion()
            
        return jsonify("""{"status": "bad"}""")
    

@app.route('/result', methods=['GET'])
def get_result():
    global players
    return jsonify(players)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port = 5000, debug=True)


"""иметь валидацию повтороного нажатия на фронте"""