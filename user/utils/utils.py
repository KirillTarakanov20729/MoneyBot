import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('API_KEY')
async def check(message):
    if hasattr(message, 'text') and message.text in await get_list_categories():
        return True
    else:
        return False

async def get_list_categories():
    categories = [
        'Еда 🍔',
        'Жилье 🏠',
        'Транспорт 🚘',
        'Развлечение 🎪',
        'Одежда и обувь 👠',
        'Здоровье и красота 💅',
        'Образование 📕',
        'Электроника 📱',
        'Подарки 🎁'
    ]
    return categories

async def get_name_of_month(number):
    if number == 1:
        return 'Январь'
    elif number == 2:
        return 'Февраль'
    elif number == 3:
        return 'Март'
    elif number == 4:
        return 'Апрель'
    elif number == 5:
        return 'Май'
    elif number == 6:
        return 'Июнь'
    elif number == 7:
        return 'Июль'
    elif number == 8:
        return 'Август'
    elif number == 9:
        return 'Сентябрь'
    elif number == 10:
        return 'Октябрь'
    elif number == 11:
        return 'Ноябрь'
    elif number == 12:
        return 'Декабрь'

async def generate_text(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            messages=[
                {"role": "user", "content": "Приведи интересные советы как можно экономить. Проведи краткий анализ моих расходов и сделай вывод, на что нужно больше тратить, а на что меньше. Приведи пару интересных фактов на основе моих данных. Все суммы указаны в рублях" + prompt}
            ]
        )
        return response['choices'][0]['message']['content']