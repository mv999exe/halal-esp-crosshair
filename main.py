import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QColorDialog, QCheckBox
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class CrosshairWindow(QMainWindow):
    def __init__(self, color=Qt.green, scale=1.0, is_dynamic=False):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        self.color = color
        self.scale = scale
        self.is_dynamic = is_dynamic

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, max(1, int(3 * self.scale)))
        painter.setPen(pen)

        screen_width = self.width()
        screen_height = self.height()
        center_x, center_y = screen_width // 2, screen_height // 2

        head_radius = int(15 * self.scale)  # Head radius
        body_height = int(60 * self.scale)  # Body length
        arm_length = int(40 * self.scale)  # Arm length
        leg_length = int(30 * self.scale)  # Leg length

        painter.drawEllipse(center_x - head_radius, center_y - head_radius, head_radius * 2, head_radius * 2)

        painter.drawLine(center_x, center_y + head_radius, center_x, center_y + head_radius + body_height)

        arm_y_start = center_y + head_radius + body_height // 4
        arm_x_offset = int(30 * self.scale)
        painter.drawLine(center_x, arm_y_start, center_x - arm_x_offset, arm_y_start + int(20 * self.scale))
        painter.drawLine(center_x, arm_y_start, center_x + arm_x_offset, arm_y_start + int(20 * self.scale))

        leg_y_start = center_y + head_radius + body_height
        leg_x_offset = int(20 * self.scale)
        painter.drawLine(center_x, leg_y_start, center_x - leg_x_offset, leg_y_start + leg_length)
        painter.drawLine(center_x, leg_y_start, center_x + leg_x_offset, leg_y_start + leg_length)

        if self.is_dynamic:
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(center_x - 10, center_y, center_x + 10, center_y)
            painter.drawLine(center_x, center_y - 10, center_x, center_y + 10)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crosshair Controller")
        self.setGeometry(300, 200, 600, 500)
        self.setStyleSheet("background-color: #1E1E1E; color: #E0E0E0;")
        self.crosshair_window = None

        self.crosshair_color = Qt.green
        self.crosshair_scale = 1.0
        self.crosshair_dynamic = False

        self.init_ui()

    def init_ui(self):
        title = QLabel("Crosshair Controller", self)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00FF00;")

        self.toggle_button = QPushButton("Enable Crosshair")
        self.toggle_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.toggle_button.clicked.connect(self.toggle_crosshair)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.exit_button.clicked.connect(self.close_application)

        size_label = QLabel("Crosshair Scale:")
        size_label.setStyleSheet("color: #FFFFFF;")
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(int(self.crosshair_scale * 10))
        self.size_slider.setStyleSheet("color: #FFFFFF;")
        self.size_slider.valueChanged.connect(self.update_crosshair_scale)

        self.color_button = QPushButton("Change Crosshair Color")
        self.color_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.color_button.clicked.connect(self.change_crosshair_color)

        self.dynamic_checkbox = QCheckBox("Enable Dynamic Crosshair")
        self.dynamic_checkbox.setStyleSheet("color: #FFFFFF;")
        self.dynamic_checkbox.stateChanged.connect(self.toggle_dynamic_crosshair)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(size_label)
        slider_layout.addWidget(self.size_slider)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addStretch()
        layout.addLayout(slider_layout)
        layout.addWidget(self.color_button)
        layout.addWidget(self.dynamic_checkbox)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.exit_button)
        layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_crosshair(self):
        if self.crosshair_window is None:
            self.crosshair_window = CrosshairWindow(color=self.crosshair_color, scale=self.crosshair_scale, is_dynamic=self.crosshair_dynamic)
            self.crosshair_window.show()
            self.toggle_button.setText("Disable Crosshair")
        else:
            self.crosshair_window.close()
            self.crosshair_window = None
            self.toggle_button.setText("Enable Crosshair")

    def update_crosshair_scale(self, value):
        self.crosshair_scale = value / 10.0
        if self.crosshair_window:
            self.crosshair_window.scale = self.crosshair_scale
            self.crosshair_window.update()

    def change_crosshair_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.crosshair_color = color
            if self.crosshair_window:
                self.crosshair_window.color = self.crosshair_color
                self.crosshair_window.update()

    def toggle_dynamic_crosshair(self, state):
        self.crosshair_dynamic = state == Qt.Checked
        if self.crosshair_window:
            self.crosshair_window.is_dynamic = self.crosshair_dynamic
            self.crosshair_window.update()

    def close_application(self):
        if self.crosshair_window:
            self.crosshair_window.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
