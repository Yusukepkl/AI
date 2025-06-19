import requests
from config import config
from logger import logger
from typing import Dict, List

RASA_URL = config.RASA_URL

def interpret(text: str) -> Dict[str, List]:
    """
    Chama o Rasa NLU e retorna um dict com keys 'intent' (str) e 'entities' (list).
    Nunca retorna None.
    """
    try:
        r = requests.post(RASA_URL, json={'text': text})
        data = r.json()
        intent = data.get('intent', {}).get('name', '')
        entities = data.get('entities', [])
        logger.info(f'Rasa parsed intent={intent}, entities={entities}')
        return {'intent': intent, 'entities': entities}
    except Exception as e:
        logger.error(f'Error calling Rasa NLU: {e}')
        return {'intent': '', 'entities': []}  # nunca retorna None

def handle(parsed: Dict[str, List]) -> str:
    """
    Gera a resposta baseada no intent e entities extraídos.
    Retorna string vazia para fallback, nunca None.
    """
    intent = parsed.get('intent', '')
    entities = parsed.get('entities', [])

    if intent == 'greet':
        return 'Olá! Em que posso ajudar?'
    if intent == 'goodbye':
        return 'Até logo!'
    if intent == 'thank_you':
        return 'Por nada!'
    if intent == 'schedule_meeting':
        date = next((e['value'] for e in entities if e.get('entity') == 'date'), None)
        return f'Agendarei reunião em {date}.' if date else 'Para qual data você quer agendar?'

    # Fallback para casos não reconhecidos
    return ''  # fallback, não retorna None
