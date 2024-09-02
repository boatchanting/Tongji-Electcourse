import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from selectcourse_settings import SettingsWindow 
from selectcourse import SelectCourseWindow 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建主窗口的垂直布局
        layout = QVBoxLayout()

        # 创建并添加 "配置" 界面
        self.settings_window = SettingsWindow()
        layout.addWidget(self.settings_window)

        # 创建并添加 "蹲课" 界面
        self.select_course_window = SelectCourseWindow()
        layout.addWidget(self.select_course_window)

        # 设置布局
        self.setLayout(layout)

        # 设置主窗口标题和大小
        self.setWindowTitle('蹲课器')
        self.setGeometry(300, 300, 600, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
