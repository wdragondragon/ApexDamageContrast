import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QCheckBox


class DisclaimerWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.check_box = QCheckBox('已阅', self)

        self.setWindowTitle('声明')
        self.setGeometry(100, 100, 1000, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.set_disclaimer_text()

        self.show_disclaimer_message()

    def set_disclaimer_text(self):
        disclaimer = '''本软件由Jdragon友情提供，apex更多数据请关注抖音：Apex [IMC] Jdragon)'''
        self.disclaimer_text = disclaimer

    def show_disclaimer_message(self):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle('声明')

        message_box.setText(self.disclaimer_text)
        message_box.setCheckBox(self.check_box)

        confirm_button = message_box.addButton('确认', QMessageBox.AcceptRole)
        confirm_button.clicked.connect(self.check_and_accept)

        message_box.exec_()

    def check_and_accept(self):
        if self.check_box.isChecked():
            self.close()
        else:
            QMessageBox.warning(self, '警告', '请先勾选同意免责声明', QMessageBox.Ok)
            self.show_disclaimer_message()
