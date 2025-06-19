# -- vad.py
import webrtcvad
from logger import logger

def init_vad(mode: int = 1) -> webrtcvad.Vad:
    """
    Inicializa o VAD com o modo especificado (0-3).
    """
    vad = webrtcvad.Vad(mode)
    logger.info(f'VAD initialized with mode {mode}')
    return vad


def vad_collector(vad: webrtcvad.Vad, frames: list[bytes], sample_rate: int = 16000,
                  frame_ms: int = 30, padding_ms: int = 300):
    """
    Gera segmentos de áudio voz a partir de uma lista de frames brutos.

    Parâmetros:
      vad        : instância do VAD
      frames     : lista de bytes (PCM 16-bit)
      sample_rate: taxa de amostragem em Hz
      frame_ms   : duração de cada frame em ms
      padding_ms : duração de preenchimento para detecção

    Retorna:
      Iterador de segmentos de áudio de voz (bytes concatenados).
    """
    num_padding = int(padding_ms / frame_ms)
    ring_buffer: list[bytes] = []
    voiced_frames: list[bytes] = []
    triggered = False

    for frame in frames:
        if not triggered:
            # Avalia se o frame atual contém fala
            if vad.is_speech(frame, sample_rate):
                ring_buffer.append(frame)
            else:
                ring_buffer.append(frame)
            if sum(vad.is_speech(f, sample_rate) for f in ring_buffer) > 0.9 * num_padding:
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
            ring_buffer.append(frame)
            if sum(vad.is_speech(f, sample_rate) for f in ring_buffer) > 0.9 * num_padding:
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            if sum(not vad.is_speech(f, sample_rate) for f in ring_buffer) > num_padding:
                logger.debug('Yielding VAD segment')
                yield b''.join(voiced_frames)
                ring_buffer.clear()
                voiced_frames.clear()
                triggered = False

    # Se ainda restarem frames de voz ao final, retorna
    if voiced_frames:
        yield b''.join(voiced_frames)
