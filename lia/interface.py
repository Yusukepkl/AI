# interface.py
import threading
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QSplitter,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from lia.robotface import RobotFace  # Classe de rosto animado


class MainWindow(QMainWindow):
    def __init__(self, send_callback):
        super().__init__()
        self.setWindowTitle("Lia Virtual Assistant")
        self.resize(1200, 800)

        # Divisor principal (horizontal)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Sidebar de plugins e status
        side = QWidget()
        sl = QVBoxLayout()
        sl.addWidget(QLabel("Plugins e Status"))
        self.plist = QListWidget()
        sl.addWidget(self.plist)
        side.setLayout(sl)
        splitter.addWidget(side)

        # --- Área central (rosto + chat + input)
        cen = QWidget()
        cl = QVBoxLayout()
        # Rosto animado
        self.face = RobotFace()
        cl.addWidget(self.face, stretch=2)
        # Chat
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        cl.addWidget(self.chat, stretch=3)
        # Barra de input
        hb = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setFont(QFont("Arial", 14))
        self.btn = QPushButton("Enviar")
        hb.addWidget(self.input)
        hb.addWidget(self.btn)
        cl.addLayout(hb)
        cen.setLayout(cl)
        splitter.addWidget(cen)

        # --- Painel de logs
        logw = QWidget()
        ll = QVBoxLayout()
        ll.addWidget(QLabel("Logs"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        ll.addWidget(self.log)
        logw.setLayout(ll)
        splitter.addWidget(logw)

        splitter.setStretchFactor(1, 5)
        self.setCentralWidget(splitter)

        # Conecta botões ao envio
        self.btn.clicked.connect(lambda: self._send(send_callback))
        self.input.returnPressed.connect(lambda: self._send(send_callback))

    def _send(self, callback):
        """
        Captura o texto do usuário e dispara o callback em uma thread separada.
        """
        text = self.input.text().strip()
        if not text:
            return
        self.chat.append(f"<b>Você:</b> {text}")
        self.input.clear()
        threading.Thread(target=callback, args=(text,), daemon=True).start()

    def append_response(self, text):
        """
        Insere no chat a resposta da Lia e anima o rosto.
        """
        self.face.animate("speaking", "happy")
        self.chat.append(f"<b>Lia:</b> {text}")
        self.face.animate("idle", "neutral")

    def append_log(self, text):
        """
        Adiciona uma linha ao painel de logs.
        """
        self.log.append(text)
