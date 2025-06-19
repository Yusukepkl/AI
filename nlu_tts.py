# nlu_tts.py
import openai
import pyttsx3
from config import config
from logger import logger, tracer
from context import save_message, get_history, save_memory, summarize_history
from translation import translate
from fallback_nlu import interpret, handle
from dialog_manager import DialogManager
from plugins.loader import load_plugins

# Configura OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# Carrega plugins dinamicamente da pasta 'plugins'
plugins = load_plugins('plugins')

# Mapeamento de emoções por palavras-chave
KEYWORD_EMOTIONS = {
    'te amo': 'happy', 'eu te amo': 'happy', 'amo você': 'happy',
    'oi vida': 'excited', 'olá': 'happy', 'bom dia': 'happy',
    'boa tarde': 'happy', 'boa noite': 'calm',
    'obrigado': 'grateful', 'obrigada': 'grateful', 'muito obrigado': 'grateful',
    'desculpa': 'sorry', 'me desculpe': 'sorry',
    'triste': 'sad', 'não estou bem': 'sad',
    'tchau': 'calm', 'até logo': 'calm', 'até mais': 'calm',
    'parabéns': 'excited', 'feliz aniversário': 'excited',
    'como você está': 'curious', 'tudo bem': 'curious',
}

def detect_emotion(text: str) -> str:
    """
    Identifica emoção básica a partir de palavras-chave.
    """
    t = text.lower()
    for key, emo in KEYWORD_EMOTIONS.items():
        if key in t:
            return emo
    return 'neutral'


def process_loop(command_q, text_q, response_q, vis_callback=None):
    """
    Loop principal que:
      1. Recebe texto (prioriza comandos de hotword)
      2. Salva no histórico e sumariza se necessário
      3. Processa plugins customizados
      4. Se sem resposta dos plugins, usa Rasa ou OpenAI
      5. Realiza TTS e retorna resposta
    """
    engine = pyttsx3.init()
    dm = DialogManager()

    while True:
        # 1. Captura entrada: hotword ou texto livre
        user_text = command_q.get() if not command_q.empty() else text_q.get()
        save_message('user', user_text)
        summarize_history()

        # 2. Memória de longo prazo: comandos específicos
        if any(k in user_text.lower() for k in ['lembre-me', 'meu aniversário']):
            save_memory('nota_usuario', user_text)

        # 3. Detecta emoção para animação facial
        emotion = detect_emotion(user_text)

        # 4. Tradução para inglês (Rasa usa EN)
        user_text_en = translate(user_text, dest='en')

        # 5. Tenta plugins primeiro
        reply = None
        for plugin in plugins:
            try:
                result = plugin.handle(user_text)
                if result:
                    reply = result
                    logger.info(f"Plugin {plugin.name} respondeu: {reply}")
                    break
            except Exception as e:
                logger.error(f"Erro no plugin {plugin.name}: {e}")

        # 6. Se sem resposta, passa para NLU
        if not reply:
            parsed = interpret(user_text_en)
            intent = parsed.get('intent', '')
            if intent:
                reply = handle(parsed)
                logger.info(f'Rasa intent tratado: {intent}')
            else:
                # Contexto + OpenAI
                history = get_history(limit=len(config.LANGUAGES))
                messages = [{'role': r, 'content': c} for r, c in history]
                messages.extend(dm.get_msgs(user_text))
                with tracer.start_as_current_span('openai_nlu'):
                    resp = openai.ChatCompletion.create(
                        model='gpt-4o-mini',
                        messages=messages
                    )
                reply = resp.choices[0].message.content
                logger.info('OpenAI respondeu ao NLU')

        # 7. Salva resposta e faz TTS
        save_message('assistant', reply)
        if vis_callback:
            vis_callback(state='speaking', emotion=emotion)
        engine.say(reply)
        engine.runAndWait()
        if vis_callback:
            vis_callback(state='idle', emotion=emotion)

        # 8. Enfileira para UI/WebSocket
        response_q.put(reply)
