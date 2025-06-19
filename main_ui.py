import sys
import queue
import threading
from PySide6.QtWidgets import QApplication
from interface import MainWindow
from hotword import listen_hotwired
from asr import transcribe
from nlu_tts import process_loop
from kafka_pipeline import start_kafka_consumer

if __name__ == "__main__":
    # Filas de comunicação
    cmd_q = queue.Queue()
    aud_q = queue.Queue()
    txt_q = queue.Queue()
    resp_q = queue.Queue()

    # Inicializa GUI
    app = QApplication(sys.argv)
    window = MainWindow(lambda t: cmd_q.put(t))

    # 1) Hotword listener → coloca “WAKE” em cmd_q e segmentos de áudio em aud_q
    threading.Thread(
        target=listen_hotwired, args=(cmd_q, aud_q, window.face.animate), daemon=True  # sem parâmetro "keyword"
    ).start()

    # 2) ASR: consome aud_q, produz txt_q
    threading.Thread(target=transcribe, args=(aud_q, txt_q), daemon=True).start()

    # 3) NLU + TTS: consome cmd_q e txt_q, produz resp_q
    threading.Thread(target=process_loop, args=(cmd_q, txt_q, resp_q, window.face.animate), daemon=True).start()

    # 4) Kafka logs → exibe no painel de logs
    def kafka_log(message):
        window.append_log(f"Kafka: {message}")

    threading.Thread(target=start_kafka_consumer, args=("lia_audio", kafka_log), daemon=True).start()

    # 5) Poll de respostas da AI → exibe no chat
    def poll_responses():
        while True:
            response = resp_q.get()
            window.append_response(response)

    threading.Thread(target=poll_responses, daemon=True).start()

    # 6) Executa a aplicação
    window.show()
    sys.exit(app.exec())
