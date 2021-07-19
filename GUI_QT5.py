import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import get_follows_info
import no_api
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import (QFont,QPixmap)

win_title = "信息推荐系统demo"
# widgets模块包含创造经典桌面风格的用户界面提供了一套UI元素的类。
class ui_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.user_info={}
        #self.btn_confirm = QtWidgets.QPushButton("确定", self)#确认发送uid
        self.text = QtWidgets.QLineEdit('在这里输入uid', self)
        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.resize(1000, 800)
        self.setWindowTitle(win_title)
        self.setWindowIcon(QtGui.QIcon('icon_bilibili.png'))
        self.btn_confirm = QtWidgets.QPushButton("确定", self)  # 确认发送uid

        self.btn_confirm.setToolTip('<b>点击这里发送uid\t</b>')
        self.btn_confirm.clicked.connect(lambda: self.send_info())

        self.text.selectAll()
        self.text.setFocus()
        # self.text.setGeometry(250, 150, 150, 30)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.text)
        hbox1.addStretch(1)
        hbox1.addWidget(self.btn_confirm)
        hbox1.addStretch(5)

        pixmap = QPixmap("icon_bilibili.png")
        lbl = QtWidgets.QLabel(self)
        lbl.setPixmap(pixmap)
        # vbox.addWidget(lbl)
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(lbl)
        hbox2.addStretch(1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(5)


        self.setLayout(vbox)
        self.show()

    def send_info(self):
        uid_t = self.text.text()
        if uid_t.isdigit():
            uid = int(uid_t)
            self.user_info=no_api.func_user_info(int(uid))
            print("----定位1----")

    def paintEvent(self, event):  # 绘图事件
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(255, 113, 109))
        qp.setFont(QtGui.QFont('Decorative', 50))
        # 没写完
        qp.drawText(event.rect(), Qt.AlignHCenter, "信息推荐系统")






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui_w = ui_window()
    '''
    widget = QtWidgets.QWidget()
    widget.resize(360, 360)
    widget.setWindowTitle(win_title)
    widget.show()
    '''
    sys.exit(app.exec())

