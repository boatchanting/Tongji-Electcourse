import sys
import os
import pyautogui
import time
import threading
import keyboard  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox, QSlider
from PyQt5.QtCore import Qt

class SelectCourseWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        self.is_testing = False
        self.coordinates = []
        self.click_thread = None  # 用于保存点击线程的引用
        self.keyboard_thread = threading.Thread(target=self.keyboard_listener)  # 键盘监听线程
        self.keyboard_thread.daemon = True  # 设置为守护线程，主程序退出时自动关闭
        self.keyboard_thread.start()

    def initUI(self):
        self.setWindowTitle('蹲课器')
        self.setGeometry(300, 300, 400, 200)
        
        # 设置窗口背景为浅蓝渐变色
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(90deg, #B2EBF2 0%, #81D4FA 100%);
                font-size: 20px;
            }
        """)
        
        vbox = QVBoxLayout()
        
        # 美化下拉框
        self.input_combo_box = RefreshableComboBox(self)  # 使用自定义的 RefreshableComboBox
        self.input_combo_box.setEditable(True)
        self.input_combo_box.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #81D4FA;
                border-radius: 10px;
                font-size: 20px;
            }
            QComboBox::drop-down {
                border-radius: 10px;
            }
            QComboBox QAbstractItemView {
                border-radius: 10px;
                background-color: #B2EBF2;
                selection-background-color: #81D4FA;
                padding: 5px;
            }
        """)
        vbox.addWidget(self.input_combo_box)
        
        self.status_label = QLabel(self)
        vbox.addWidget(self.status_label)
        
        # 添加滑动条用于设置停顿时间
        hbox_slider = QHBoxLayout()
        self.pause_slider = QSlider(Qt.Horizontal, self)
        self.pause_slider.setMinimum(5)
        self.pause_slider.setMaximum(30)
        self.pause_slider.setValue(10)
        self.pause_slider.setTickPosition(QSlider.TicksBelow)
        self.pause_slider.setTickInterval(1)
        self.pause_slider.valueChanged.connect(self.update_slider_label)
        hbox_slider.addWidget(QLabel("停顿时间 (秒):"))
        hbox_slider.addWidget(self.pause_slider)
        
        self.slider_value_label = QLabel(f"{self.pause_slider.value()}秒", self)
        hbox_slider.addWidget(self.slider_value_label)
        vbox.addLayout(hbox_slider)
        
        hbox = QHBoxLayout()
        
        # 设置圆角按钮
        self.start_button = QPushButton('启动(Ctrl+B)', self)
        self.start_button.clicked.connect(self.start_test)
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
        hbox.addWidget(self.start_button)
        
        self.stop_button = QPushButton('停止(Ctrl+E)', self)
        self.stop_button.clicked.connect(self.stop_test)
        self.stop_button.setStyleSheet("""
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
        hbox.addWidget(self.stop_button)
        
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)

    def start_test(self):
        if self.is_testing:
            return
        
        file_name = self.input_combo_box.currentText()
        if not file_name:
            self.show_error("请输入配置文件")
            return
        
        file_path = f'./settings/{file_name}.txt'
        if not os.path.exists(file_path):
            self.show_error("找不到你的文件，请输入正确的文件名或者从下拉选项中选择")
            return
        
        self.coordinates = self.read_coordinates(file_path)
        self.is_testing = True
        self.click_thread = threading.Thread(target=self.run_clicks)
        self.click_thread.start()

    def stop_test(self):
        if self.is_testing:
            self.is_testing = False
            self.status_label.setText("蹲课器已经停止")
    
    def run_clicks(self):
        i = 1  # 轮数计数器
        try:
            while self.is_testing:
                for j, coord in enumerate(self.coordinates):
                    if not self.is_testing:
                        break
                    pyautogui.moveTo(coord[0], coord[1], duration=0.5)
                    pyautogui.click(coord[0], coord[1])
                    self.status_label.setText(f"第{i}轮，第{j+1}次点击")
                    
                    if j == 0:
                        time.sleep(1)
                    elif j == 1:
                        time.sleep(5)
                
                if not self.is_testing:
                    break

                self.status_label.setText(f"第{i}轮完成")
                i += 1
                
                pause_time = self.pause_slider.value()
                time.sleep(pause_time)
        
        except Exception as e:
            self.show_error(f"发生错误: {str(e)}")
        
        self.is_testing = False

    def read_coordinates(self, file_path):
        coordinates = []
        with open(file_path, 'r') as file:
            for line in file:
                coord = line.strip('() \n').split(',')
                coordinates.append((int(coord[0]), int(coord[1])))
        return coordinates
    
    def show_error(self, message):
        QMessageBox.critical(self, "错误", message)
        self.status_label.setText(message)
    
    def update_slider_label(self):
        self.slider_value_label.setText(f"{self.pause_slider.value()}秒")
    
    def keyboard_listener(self):
        while True:
            if keyboard.is_pressed('ctrl+b') and not self.is_testing:
                self.start_test()
            elif keyboard.is_pressed('ctrl+e') and self.is_testing:
                self.stop_test()
            time.sleep(0.1)

class RefreshableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def showPopup(self):
        self.clear()  # 清空下拉选项
        self.load_files_to_combobox()  # 重新加载文件列表
        super().showPopup()  # 显示下拉选项

    def load_files_to_combobox(self):
        settings_dir = './settings'
        if os.path.exists(settings_dir):
            for file_name in os.listdir(settings_dir):
                if file_name.endswith('.txt'):
                    self.addItem(file_name[:-4])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SelectCourseWindow()
    ex.show()
    sys.exit(app.exec_())
