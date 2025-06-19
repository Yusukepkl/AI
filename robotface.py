# robotface.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QBrush, QCursor
from PySide6.QtCore import QTimer, QRectF, Qt
import math

class RobotFace(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.state, self.emotion = 'idle', 'neutral'
        self.blink = False
        self.breath = 0.0

        # Blink timer
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self._trigger_blink)
        self.blink_timer.start(5000)
        self.blink_close_timer = QTimer(self)
        self.blink_close_timer.setSingleShot(True)
        self.blink_close_timer.timeout.connect(self._end_blink)

        # Breathe animation
        self.breathe_timer = QTimer(self)
        self.breathe_timer.timeout.connect(self._update_breath)
        self.breathe_timer.start(100)

        # Repaint loop
        self.repaint_timer = QTimer(self)
        self.repaint_timer.timeout.connect(self.update)
        self.repaint_timer.start(50)

    def _trigger_blink(self):
        self.blink = True
        self.blink_close_timer.start(150)

    def _end_blink(self):
        self.blink = False

    def _update_breath(self):
        self.breath = (self.breath + 0.1) % (math.pi * 2)

    def animate(self, state, emotion='neutral'):
        """
        Atualiza o estado e emoção para animações.
        """
        self.state = state
        self.emotion = emotion

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        painter.fillRect(self.rect(), QColor(15, 15, 25))

        # Face base (pulsa com respiração)
        scale = 1 + 0.02 * math.sin(self.breath)
        fw, fh = w * 0.8 * scale, h * 0.8 * scale
        fx, fy = (w - fw) / 2, (h - fh) / 2

        # Cor depende de estado e emoção
        base = QColor(50, 150, 200) if self.state == 'idle' else QColor(80, 200, 150)
        if self.emotion == 'happy':
            fc = base.lighter(130)
        elif self.emotion == 'thinking':
            fc = base.darker(130)
        elif self.emotion == 'excited':
            fc = QColor(255, 180, 100)
        elif self.emotion == 'grateful':
            fc = QColor(200, 200, 100)
        elif self.emotion == 'sad':
            fc = QColor(100, 100, 200)
        elif self.emotion == 'sorry':
            fc = QColor(200, 100, 100)
        elif self.emotion == 'curious':
            fc = QColor(150, 100, 200)
        else:
            fc = base

        painter.setBrush(QBrush(fc))
        painter.drawEllipse(int(fx), int(fy), int(fw), int(fh))

        # Boca (fala ou neutra)
        mw = fw * 0.3
        mh = fh * 0.07 if self.state == 'speaking' else fh * 0.03
        mx, my = fx + (fw - mw) / 2, fy + fh * 0.65
        painter.setBrush(QBrush(QColor(255, 80, 80)))
        painter.drawRoundedRect(QRectF(int(mx), int(my), int(mw), int(mh)), 10, 10)

        # Olhos
        er = fw * 0.1
        pr = er * 0.4
        cursor = self.mapFromGlobal(QCursor.pos())
        painter.setPen(Qt.PenStyle.NoPen)
        for xp in (0.3, 0.7):
            ex, ey = fx + fw * xp, fy + fh * 0.35
            # Brilho do olho
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(int(ex - er), int(ey - er / 2), int(er), int(er / 1.5))
            # Pupila segue cursor
            dx = max(-1.0, min(1.0, (cursor.x() - ex) / (fw * 0.5)))
            dy = max(-1.0, min(1.0, (cursor.y() - ey) / (fh * 0.5)))
            px, py = ex + dx * (pr * 0.5), ey + dy * (pr * 0.5)
            painter.setBrush(QBrush(QColor(10, 10, 10)))
            painter.drawEllipse(int(px - pr / 2), int(py - pr / 2), int(pr), int(pr))
