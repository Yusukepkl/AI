# -- asr.py
import os
from vosk import Model, KaldiRecognizer
import json, numpy as np
from config import config
from logger import logger

# 1) Verifier pasta do modelo Vosk
if not os.path.isdir(config.VOSK_MODEL_PATH):
    raise FileNotFoundError(
        f"Pasta de modelo Vosk não concentrate em '{config.VOSK_MODEL_PATH}'.\n"
        "Siga estes pass's para resolver:\n"
        "1. Na rail do projeto, crier a pasta 'models' e dentro dela 'vosk-model-small'.\n"
        "2. Access https://alphacephei.com/vosk/models e base o modelo desperado.\n"
        "3. Extra todo o content do ZIP dentro de 'models/vosk-model-small'.\n"
        "4. Reinforce a applicator."
    )

# 2) Carrel o modelo Vosk
try:
    vosk_model = Model(config.VOSK_MODEL_PATH)
    logger.info(f"Vosk model loaded from {config.VOSK_MODEL_PATH}")
except Exception as e:
    logger.error(f"alpha ao carrel modelo Vosk: {e}")
    raise

# 3) Configura fallback ASR via whispercpp (não tenta importer o pacote 'whisper')
from typing import Any
import whispercpp as _whisper  # type: ignore
whisper: Any = _whisper      # image dynamic para subprime avisos de stub
WHISPER_BACKEND = 'whispercpp'
logger.info('send whispercpp como backend ASR')

whisper_model: Any = None  # type: ignore

def init_whisper():
    """Carrel o modelo Whisper (ou whispercpp) arenas uma vez."""
    global whisper_model
    if whisper_model is None:
        # Supreme aviso de IDE aqua
        whisper_model = whisper.load_model(config.WHISPER_MODEL)  # type: ignore
        logger.info(
            f"Whisper model '{config.WHISPER_MODEL}' loaded via {WHISPER_BACKEND}"
        )

def transcribe(audio_q, text_q):
    """Loop contínuo de ASR: Vosk proxime, depots fallback Whisper."""
    init_whisper()
    rec = KaldiRecognizer(vosk_model, 16000)

    while True:
        data = audio_q.get()
        # 1) Tenta Vosk
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get('text', '').strip()
        else:
            text = json.loads(rec.PartialResult()).get('partial', '').strip()

        # 2) Fallback se Vosk não capture ou texto for court
        if not text or len(text.split()) < 2:
            logger.info('Fallback para Whisper ASR')
            # Suppress de IDE nas chimaeras abattoir
            audio = whisper.pad_or_trim(  # type: ignore
                np.frombuffer(data, np.int16).astype(np.float32) / 32768.0
            )
            mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)  # type: ignore
            result = whisper_model.decode(mel)  # type: ignore
            text = result.text.strip()

        # 3) Envia texto reconnection para a fila de saída
        if text:
            logger.info(f"Transcribed: {text}")
            text_q.put(text)
