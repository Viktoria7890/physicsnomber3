import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# Холст для графика
class CustomCanvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)

# Главное окно
class CycloidSimulator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем заголовок и размер окна
        self.setWindowTitle("Модель движения на ободе")
        self.setGeometry(200, 200, 900, 650)

        # Метки и поля ввода
        self.radius_label = QLabel("Радиус колеса (r):", self)
        self.radius_input = QLineEdit(self)

        self.velocity_label = QLabel("Скорость центра масс (v):", self)
        self.velocity_input = QLineEdit(self)

        # Кнопка с измененным цветом
        self.visualize_button = QPushButton("Построить траекторию", self)
        self.visualize_button.setStyleSheet(
            "background-color: lightgreen; color: black; font-weight: bold;"
        )
        self.visualize_button.clicked.connect(self.draw_trajectory)

        # Настраиваем холст для графиков
        self.canvas = CustomCanvas(self, width=5, height=4, dpi=100)

        # Размещение элементов на экране
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.radius_label)
        form_layout.addWidget(self.radius_input)
        form_layout.addWidget(self.velocity_label)
        form_layout.addWidget(self.velocity_input)
        form_layout.addWidget(self.visualize_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.canvas)

        # Устанавливаем основной виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Метод для отрисовки графика
    def draw_trajectory(self):
        try:
            # Получение и проверка значений радиуса и скорости
            radius = float(self.radius_input.text())
            velocity = float(self.velocity_input.text())
            if radius <= 0 or velocity <= 0:
                raise ValueError

            # Вычисление параметров для траектории
            omega = velocity / radius
            time_values = np.linspace(0, 4 * np.pi, 500)
            x_values = radius * (omega * time_values - np.sin(omega * time_values))
            y_values = radius * (1 - np.cos(omega * time_values))

            # Очистка предыдущего графика
            self.canvas.ax.clear()

            # Построение новой траектории
            self.canvas.ax.plot(x_values, y_values, color='navy', lw=2, label="Траектория")
            self.canvas.ax.set_title("Циклоида: Движение точки на колесе", fontsize=12)
            self.canvas.ax.set_xlabel("Положение X")
            self.canvas.ax.set_ylabel("Положение Y")

            # Настраиваем сетку и легенду
            self.canvas.ax.grid(True, which='both', linestyle='--', linewidth=0.7)
            self.canvas.ax.axhline(0, color='black', linewidth=0.8)
            self.canvas.ax.axvline(0, color='black', linewidth=0.8)
            self.canvas.ax.legend()

            # Обновляем холст
            self.canvas.draw()

        except ValueError:
            print("Ошибка: Введите корректные положительные значения радиуса и скорости.")

# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CycloidSimulator()
    window.show()
    sys.exit(app.exec_())
