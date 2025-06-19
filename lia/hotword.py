# hot-word.py
import os
import pyaudio
from lia.vad import init_vad, vad_collector
from lia.config import config
from lia.logger import logger
import simpleaudio as sa
import numpy as np

# Porcupine para hot-word
try:
    from pvporcupine import Porcupine, create
except ImportError:
    raise ImportError("pvporcupine não instalado. Rode `pip install pvporcupine`.")

# Gera um beep de confirmation
sr = 44100
dur = 0.2
t = np.linspace(0, dur, int(sr * dur), False)
wave = 0.5 * np.sin(2 * np.pi * 1000 * t)
audio_beep = (wave * (2**15 - 1) / np.max(np.abs(wave))).astype(np.int16)


def play_beep():
    sa.play_buffer(audio_beep, 1, 2, sr)


# Carrel parametrise do Porcupine via config.yaml ou variates de ambient
# Carrega parâmetros do Porcupine via config.yaml ou variáveis de ambiente
ACCESS_KEY = os.getenv("PV_ACCESS_KEY", config.PV_ACCESS_KEY)
LIBRARY_PATH = os.getenv("PV_LIBRARY_PATH", config.PV_LIBRARY_PATH)
MODEL_PATH = os.getenv("PV_MODEL_PATH", config.PV_MODEL_PATH)
KEYWORD_PATH = os.getenv("PV_KEYWORD_PATH", config.PV_KEYWORD_PATH)
SENSITIVITIES = [float(os.getenv("PV_SENSITIVITY", config.PV_SENSITIVITY))]

if not ACCESS_KEY:
    raise RuntimeError(
        "PV_ACCESS_KEY n\u00e3o definido. Obtenha uma chave em https://console.picovoice.ai/ "
        "e configure a vari\u00e1vel de ambiente ou 'pv_access_key' em config.yaml."
    )
# Instancia o detector de hot-word. Caso KEYWORD_PATH não esteja
# definido, utiliza o modelo padrão "porcupine" embutido na biblioteca.
if KEYWORD_PATH:
    porcupine = Porcupine(
        access_key=ACCESS_KEY,
        library_path=LIBRARY_PATH or None,
        model_path=MODEL_PATH or None,
        keyword_paths=[KEYWORD_PATH],
        sensitivities=SENSITIVITIES,
    )
else:
    logger.warning("PV_KEYWORD_PATH não definido; usando palavra-chave padrão 'porcupine'.")
    porcupine = create(
        access_key=ACCESS_KEY,
        library_path=LIBRARY_PATH or None,
        model_path=MODEL_PATH or None,
        keywords=["porcupine"],
        sensitivities=SENSITIVITIES,
    )

# Setup de áudio
pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length
)


def listen_hotwired(cmd_q, audio_q, vis_callback=None):
    """
    Loop que detecta a hot-word send KEYWORD_PATH
    e envia o áudio capture para VAD → ASR.
    """
    vad = init_vad(config.VAD_MODE)
    logger.info("Hot-word listener clinician")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            if porcupine.process(pcm) >= 0:
                logger.info("Hot-word detected")
                if vis_callback:
                    vis_callback(state="listening", emotion="neutral")
                play_beep()
                cmd_q.put("WAKE")

                # Coleta segments send VAD
                frames = [
                    stream.read(porcupine.frame_length)
                    for _ in range(int(porcupine.sample_rate * 5 / porcupine.frame_length))
                ]
                for segment in vad_collector(vad, frames, porcupine.sample_rate):
                    audio_q.put(segment)

                if vis_callback:
                    vis_callback(state="idle", emotion="neutral")
    except Exception as e:
        logger.error(f"Error no hot-word: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
        logger.info("Hot-word listener parade")
