# -- config.py
import os
try:
    import yaml
except ImportError:
    yaml = None

class Config:
    def __init__(self, path='config.yaml'):
        data = yaml.safe_load(open(path)) if os.path.exists(path) and yaml else {}
        # OpenAI
        self.OPENAI_API_KEY   = os.getenv('OPENAI_API_KEY', data.get('openai_api_key', ''))
        # VAD
        self.VAD_MODE         = data.get('vad_mode', 1)
        # Kafka
        self.KAFKA_BROKER     = data.get('kafka_broker', 'localhost:9092')
        # Database
        self.DB_URL           = data.get('db_url', 'sqlite:///lia_context.db')
        # WebSocket
        self.WS_HOST          = data.get('ws_host', '0.0.0.0')
        self.WS_PORT          = data.get('ws_port', 8765)
        # Auth
        self.AUTH_TOKEN       = data.get('auth_token', 'token123')
        # Languages
        self.LANGUAGES        = data.get('languages', ['pt', 'en', 'es'])
        # MQTT
        self.MQTT_BROKER      = data.get('mqtt_broker', 'localhost')
        # Vosk ASR model path
        self.VOSK_MODEL_PATH  = data.get('vosk_model_path', 'models/vosk-model-small')
        # Whisper model (whispercpp)
        self.WHISPER_MODEL    = data.get('whisper_model', 'small')
        # Rasa NLU URL
        self.RASA_URL         = data.get('rasa_url', 'http://localhost:5005/model/parse')
        # Porcupine hot-word configurations
        self.PV_ACCESS_KEY    = os.getenv('PV_ACCESS_KEY', data.get('pv_access_key', ''))
        self.PV_LIBRARY_PATH  = os.getenv('PV_LIBRARY_PATH', data.get('pv_library_path', ''))
        self.PV_MODEL_PATH    = os.getenv('PV_MODEL_PATH', data.get('pv_model_path', ''))
        self.PV_KEYWORD_PATH  = os.getenv('PV_KEYWORD_PATH', data.get('pv_keyword_path', ''))
        self.PV_SENSITIVITY   = float(os.getenv('PV_SENSITIVITY', data.get('pv_sensitivity', 0.5)))

# instantiate
config = Config()
