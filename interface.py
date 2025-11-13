import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QProgressBar
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from config import DB_CONFIG
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ReusoAguaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reuso de Água")
        self.setStyleSheet("background-color: #121212; color: white;")
        self.setGeometry(100, 100, 1300, 700)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.titulo = QLabel("Monitoramento de Nível de Água")
        self.titulo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.titulo)

        self.botao_atualizar = QPushButton("🔄 Atualizar Leituras")
        self.botao_atualizar.setStyleSheet("background-color: #2e7d32; color: white; padding: 6px;")
        self.botao_atualizar.clicked.connect(self.atualizar_tabela)
        layout.addWidget(self.botao_atualizar)

        self.tabela = QTableWidget()
        layout.addWidget(self.tabela)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #00e676; }")
        layout.addWidget(self.progress_bar)

        self.label_status = QLabel("Nível de Água Atual:")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, distancia, volume, data_hora
                FROM leituras
                ORDER BY data_hora DESC
                LIMIT 10
            """)
            rows = cursor.fetchall()

            self.tabela.setRowCount(len(rows))
            self.tabela.setColumnCount(4)
            self.tabela.setHorizontalHeaderLabels(["ID", "Distância (cm)", "Volume (L)", "Data e Hora"])

            volumes = []

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.tabela.setItem(i, j, QTableWidgetItem(str(value)))
                volumes.append(row[2])

            if volumes:
                nivel_percentual = min(100, max(0, int((volumes[0] / max(volumes)) * 100)))
                self.progress_bar.setValue(nivel_percentual)
                self.label_status.setText(f"Nível de Água Atual: {nivel_percentual}%")

                self.plotar_grafico(volumes)
            else:
                self.label_status.setText("Sem dados disponíveis.")

            cursor.close()
            conn.close()

        except Exception as e:
            self.label_status.setText(f"Erro: {str(e)}")

    def plotar_grafico(self, volumes):
        self.ax.clear()
        self.ax.plot(range(len(volumes)), volumes, color="#00e676", marker="o")
        self.ax.set_title("Volume de Água (Últimas Leituras)")
        self.ax.set_xlabel("Leitura")
        self.ax.set_ylabel("Volume (L)")
        self.ax.grid(True, color="#333")
        self.ax.set_facecolor("#1e1e1e")
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ReusoAguaApp()
    janela.show()
    sys.exit(app.exec())
