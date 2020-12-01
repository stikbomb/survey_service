def get_data():
    data = {
                "questionnaire": 1,
                "text": "Ваш любимый город?",
                "type": "O",
                "possible_answers": [
                    {
                        "text": "Москва"
                    },
                    {
                        "text": "Воронеж"
                    },
                    {
                        "text": "Ярославль"
                    },
                    {
                        "text": "Владивосток"
                    },
                    {
                        "text": "Красноярск"
                    }
                ]
            }
    return data


def correct_create_data():
    return get_data()


def incorrect_create_data_no_possible_answers():
    data = get_data()
    data.pop('possible_answers')
    return data


def incorrect_create_data_one_possible_question():
    data = get_data()
    data['possible_answers'] = list(data['possible_answers'][0])
    return data


def incorrect_create_data_possible_answers_with_text_type_question():
    data = get_data()
    data['type'] = 'T'
    return data

def incorrect_put_data_type_field_change():
    data = get_data()
    data.pop('possible_answers')
    data['text'] = 'Ваша фамилия?'
    return data

def correct_put_data():
    data = incorrect_put_data_type_field_change()
    data['type'] = 'T'
    return data