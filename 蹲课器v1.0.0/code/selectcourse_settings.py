import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from pynput.mouse import Listener
from datetime import datetime

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('蹲课器配置')
        self.setGeometry(300, 300, 400, 200)

        # 设置窗口背景为浅蓝渐变色
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(90deg, #B2EBF2 0%, #81D4FA 100%);
                font-size: 20px;
            }
        """)

        layout = QVBoxLayout()

        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText('请输入配置名称，例如“高数”')
        self.input_line.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #81D4FA;
                border-radius: 10px;
                font-size: 20px;
            }
        """)
        layout.addWidget(self.input_line)

        self.start_button = QPushButton('进行配置(依次点击课程，保存，关闭三个按钮)', self)
        self.start_button.clicked.connect(self.start_configuration)
        self.start_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                font-size: 20px;
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #B2EBF2, stop:1 #81D4FA
                );
            }
            QPushButton:hover {
                background-color: #81D4FA;
            }
            QPushButton:pressed {
                background-color: #4FC3F7;
            }
        """)
        layout.addWidget(self.start_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_configuration(self):
        input_text = self.input_line.text()
        if not input_text:
            input_text = datetime.now().strftime('%Y%m%d%H%M')
        self.save_file_path = os.path.join('.', 'settings', f'{input_text}.txt')

        self.collect_mouse_clicks()

    def collect_mouse_clicks(self):
        self.click_positions = []

        def on_click(x, y, button, pressed):
            if pressed:
                self.click_positions.append((x, y))
                if len(self.click_positions) == 3:
                    return False

        settings_dir = os.path.dirname(self.save_file_path)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        with Listener(on_click=on_click) as listener:
            listener.join()

        if len(self.click_positions) == 3:
            self.save_click_positions()
            self.status_label.setText('配置成功！')
        else:
            QMessageBox.critical(self, '错误', '未收集到足够的点击。')

    def save_click_positions(self):
        with open(self.save_file_path, 'w') as file:
            for pos in self.click_positions:
                file.write(f'({pos[0]},{pos[1]})\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    ex.show()
    sys.exit(app.exec_())
