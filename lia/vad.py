# -- vad.py
import webrtcvad
from collections import deque
from lia.logger import logger


def init_vad(mode: int = 1) -> webrtcvad.Vad:
    """
    Inicializa o VAD com o modo especificado (0-3).
    """
    vad = webrtcvad.Vad(mode)
    logger.info(f"VAD initialized with mode {mode}")
    return vad


def vad_collector(
    vad: webrtcvad.Vad, frames: list[bytes], sample_rate: int = 16000, frame_ms: int = 30, padding_ms: int = 300
):
    """Gera segmentos de fala a partir de frames PCM."""

    num_padding = int(padding_ms / frame_ms)
    ring_buffer: deque[tuple[bytes, bool]] = deque(maxlen=num_padding)
    voiced_frames: list[bytes] = []
    triggered = False

    for frame in frames:
        is_speech = vad.is_speech(frame, sample_rate)
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([1 for _, speech in ring_buffer if speech])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                voiced_frames.extend(f for f, _ in ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([1 for _, speech in ring_buffer if not speech])
            if num_unvoiced > ring_buffer.maxlen:
                logger.debug("Yielding VAD segment")
                yield b"".join(voiced_frames)
                ring_buffer.clear()
                voiced_frames.clear()
                triggered = False

    if voiced_frames:
        yield b"".join(voiced_frames)
