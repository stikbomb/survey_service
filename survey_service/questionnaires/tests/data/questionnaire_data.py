def get_data():

    data = {
        "title": "Разные типы возрастов",
        "beginning_date": "2020-11-11",
        "expiration_date": "2020-12-12",
        "description": "Пробуем разные типа вопросов",
        "questions": [
            {
                "text": "Как Вас зовут?",
                "type": "T",
                "possible_answers": []
            },
            {
                "text": "Сколько Вам лет?",
                "type": "O",
                "possible_answers": [
                    {
                        "text": "18-25"
                    },
                    {
                        "text": "26-35"
                    },
                    {
                        "text": "36-45"
                    },
                    {
                        "text": "46+"
                    }
                ]
            },
            {
                "text": "Ваши интересы?",
                "type": "M",
                "possible_answers": [
                    {
                        "text": "Дизайн"
                    },
                    {
                        "text": "IT"
                    },
                    {
                        "text": "Игры"
                    },
                    {
                        "text": "Музыка"
                    },
                    {
                        "text": "Живопись"
                    }
                ]
            }
        ]
    }
    return data


def correct_create_data():
    return get_data()


def incorrect_create_data_one_question():
    data = get_data()
    data['questions'] = data['questions'][0]
    return data


def incorrect_create_data_one_possible_answer():
    data = get_data()
    data['questions'][1]['possible_answers'] = data['questions'][1]['possible_answers'][0]
    return data


def incorrect_create_data_wrong_field_name():
    data = get_data()
    data['end_date'] = data.pop('expiration_date')


def correct_put_data():
    data = get_data()
    data.pop('questions')
    data['title'] = 'Разные типы вопросов'
    return data


def incorrect_put_data_change_beginning_date():
    data = correct_put_data()
    data['beginning_date'] = '2020-11-13'
    return data


def incorrect_put_data_nested_objects():
    data = correct_create_data()
    data['title'] = 'Разные типы вопросов'
    return data


def incorrect_put_data_wrong_expiration_date():
    data = correct_put_data()
    data['expiration_date'] = '2019-11-13'
    return data