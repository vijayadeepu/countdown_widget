import sys

from PyQt5.QtCore import Qt, QTimer, QDateTime, QPoint
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog,
    
)


class CountdownWidget(QWidget):

    def __init__(self):
        super().__init__()

        # ---------------- Timer ----------------

        self.total_seconds = 600      # 10 minutes
        self.target = QDateTime.currentDateTime().addSecs(600)
        self.finished = False

        # ---------------- Window ----------------

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(170, 58)



        # ---------------- Timer Label ----------------

        self.label = QLabel("01:00:00")

        self.label.setAlignment(Qt.AlignCenter)

        self.label.setFont(QFont("JetBrains Mono", 18, QFont.Bold))

        self.label.setStyleSheet("""
            QLabel{
                background:transparent;
                color:white;
            }
        """)

        self.label.mousePressEvent = self.editCountdown

        # ---------------- Drag Button ----------------

        self.drag_btn = QPushButton("⇕")

        self.drag_btn.setFixedSize(20,20)

        self.drag_btn.hide()

        self.drag_btn.setStyleSheet("""
        QPushButton{
            background:rgba(50,50,50,170);
            color:white;
            border:none;
            border-radius:10px;
        }

        QPushButton:hover{
            background:rgba(90,90,90,220);
        }
        """)

        self.drag_offset = QPoint()

        self.drag_btn.mousePressEvent = self.startDrag
        self.drag_btn.mouseMoveEvent = self.dragMove

        # ---------------- Close Button ----------------

        self.close_btn = QPushButton("✕")

        self.close_btn.setFixedSize(20,20)

        self.close_btn.hide()

        self.close_btn.clicked.connect(self.close)

        self.close_btn.setStyleSheet("""
        QPushButton{
            background:rgba(120,40,40,170);
            color:white;
            border:none;
            border-radius:10px;
        }

        QPushButton:hover{
            background:rgba(220,40,40,220);
        }
        """)

        # ---------------- Layout ----------------

        top = QHBoxLayout()

        top.setContentsMargins(2,2,2,0)

        top.addWidget(self.drag_btn)

        top.addStretch()

        top.addWidget(self.close_btn)

        layout = QVBoxLayout()

        layout.setContentsMargins(4,2,4,4)

        layout.setSpacing(2)

        layout.addLayout(top)

        layout.addWidget(self.label)

        self.setLayout(layout)

        # ---------------- Update Timer ----------------

        self.timer = QTimer()

        self.timer.timeout.connect(self.updateCountdown)

        self.timer.start(1000)

        self.updateCountdown()

    # -------------------------------------------------
    # Show buttons only while hovering
    # -------------------------------------------------

    def enterEvent(self, event):
        self.drag_btn.show()
        self.close_btn.show()

    def leaveEvent(self, event):
        self.drag_btn.hide()
        self.close_btn.hide()

    # -------------------------------------------------
    # Dragging
    # -------------------------------------------------

    def startDrag(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = (
                event.globalPos()
                - self.frameGeometry().topLeft()
            )
            event.accept()

    def dragMove(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(
                event.globalPos() - self.drag_offset
            )
            event.accept()

    # -------------------------------------------------
    # Click timer to edit
    # -------------------------------------------------

    def editCountdown(self, event):

        seconds, ok = QInputDialog.getInt(
            self,
            "Countdown",
            "Remaining seconds:",
            value=max(self.remainingSeconds(), 1),
            min=1,
            max=999999
        )

        if ok:
            self.total_seconds = seconds
            self.target = (
                QDateTime.currentDateTime()
                .addSecs(seconds)
            )
            self.finished = False

            self.update()

    # -------------------------------------------------
    # Remaining seconds
    # -------------------------------------------------

    def remainingSeconds(self):

        remaining = QDateTime.currentDateTime().secsTo(
            self.target
        )

        if remaining < 0:
            return 0

        return remaining

    # -------------------------------------------------
    # Update every second
    # -------------------------------------------------

    def updateCountdown(self):

        remaining = self.remainingSeconds()

        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        self.label.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

        # ---------- Color States ----------

        if remaining > 450:
            color = "white"

        elif remaining > 300:
            color = "#FFD54F"       # yellow

        elif remaining > 90:
            color = "#FF9800"       # orange

        else:
            color = "#F44336"       # red

        self.label.setStyleSheet(f"""
            QLabel{{
                background:transparent;
                color:{color};
            }}
        """)

        # ---------- Notification ----------

        if remaining == 0 and not self.finished:

            self.finished = True

            import subprocess

            subprocess.run(["notify-send","Countdown Finished","Time is up!"])
            

        self.update()
    # -------------------------------------------------
    # Draw transparent HUD and progress bar
    # -------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # ---------- Background ----------

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(20, 20, 20, 90))

        painter.drawRoundedRect(
            self.rect(),
            10,
            10
        )

        # ---------- Progress ----------

        remaining = self.remainingSeconds()

        if self.total_seconds <= 0:
            percent = 0
        else:
            percent = remaining / self.total_seconds

        # Match timer color
        
        if remaining > 450:
            progress = QColor(255, 255, 255)

        elif remaining > 300:
            progress = QColor(255, 213, 79)

        elif remaining > 90:
            progress = QColor(255, 152, 0)

        else:
            progress = QColor(244, 67, 54)

        # ---------- Track ----------

        margin = 8

        y = self.height() - 6

        width = self.width() - margin * 2

        painter.setBrush(QColor(70, 70, 70, 120))

        painter.drawRoundedRect(
            margin,
            y,
            width,
            2,
            1,
            1
        )

        # ---------- Filled progress ----------

        fill = int(width * percent)

        painter.setBrush(progress)

        painter.drawRoundedRect(
            margin,
            y,
            fill,
            2,
            1,
            1
        )

# -------------------------------------------------
# Application Entry
# -------------------------------------------------

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(True)

    widget = CountdownWidget()

    widget.setWindowTitle("Countdown")

    # Optional: start near the top-right corner.
    # Adjust or remove these values as you like.
    
    widget.move(20, 0)

    widget.show()

    sys.exit(app.exec_())
