def get_data():
    data = {
        "questionnaire": 1,
        "user": 123,
        "passed_questions": [
            {
                "question": 1,
                "type": "T",
                "answers": ["Александр"]
            },
            {
                "question": 2,
                "type": "O",
                "answers": [2]
            },
            {
                "question": 3,
                "type": "M",
                "answers": [5, 7, 9]
            }
        ]
    }

    return data


def get_alt_data():
    data = {
        "questionnaire": 1,
        "user": 123,
        "created_at": "2020-11-11 12:28",
        "title": "Общие вопрос",
        "beginning_date": "2020-11-11",
        "expiration_date": "2020-11-11",
        "description": "Очень важный тест",

        "passed_questions": [
            {
                "text": "Как Вас зовут",
                "type": "T",
                "answers": [{"text": "Настя"}]
            },
            {
                "text": "Сколько Вам лет?",
                "type": "O",
                "answers": [{"text": "26-35"}]
            },
            {
                "text": "Ваши увлечения?",
                "type": "M",
                "answers": [
                    {"text": "Дизайн"},
                    {"text": "Игры"},
                    {"text": "IT"}]
            }
        ]
    }
    return data


def correct_data():
    return get_data()


def correct_alt_data():
    return get_alt_data()