import requests
import html
from .translator import *

def trivia():
    try:
        URL = 'https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple'
        response = requests.get(URL)
        response.raise_for_status()
        trivia = response.json()
        
        questions = []
        for question in trivia['results']:
            q = question.get('question', '')
            c = question.get('correct_answer', '')
            i = question.get('incorrect_answers', [])
            if q and c and i:
                q, c = html.unescape(q), html.unescape(c)
                questions.append(translate(q))
                questions.append(translate(c))
                for answer in i:
                    answer = html.unescape(answer)
                    questions.append(translate(answer))
        return questions
    
    except requests.exceptions.RequestException as e:
        print(f'Error de solicitud: {e}')
        return None
    except KeyError as e:
        print(f'Error al acceder a una clave en el diccionario: {e}')
        return None
    except Exception as e:
        print(f'Ocurrió un error inesperado: {e}')
        return None
    