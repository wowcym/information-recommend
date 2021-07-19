# 代码参考：https://mp.weixin.qq.com/s/RiZdyUoueZl10gvNxBZTGQ
# https://github.com/taseikyo/PyQt5-Apps/blob/8c715edd3710f413932d982f8e2e24ea9ec6e9bd/google-translate/mwin.py
# 网格布局：QGridLayout
# 调试用UID：163637592（何同学）
import jieba
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qtawesome
import txt
import requests
import webbrowser
from Infor_Recommendation import recommend_4
import bilibili_api
#uid = 163637592
#uid=13101988 AK
class main_ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.toolbar=self.addToolBar('file')
        # new =QtWidgets.QAction(QtGui.QIcon("lsy.jpg"), "new", self)
        # self.toolbar.addAction(new)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1260, 900)
        self.setWindowTitle("B站信息推荐系统")
        self.setWindowIcon(QtGui.QIcon('../icon_bilibili.png'))
        # passwdLabel.setFont(QFont("Microsoft YaHei"))
        QtGui.QFontDatabase.addApplicationFont("../font2.TTF")

        self.main_widget = QtWidgets.QWidget()  # 创建主窗口部件
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.left_widget = QtWidgets.QWidget()  # 创建左侧窗口部件
        self.left_widget.setObjectName("left_widget")
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        self.right_widget = QtWidgets.QWidget()  # 创建右侧窗口部件
        self.right_widget.setObjectName("right_widget_total")
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)

        self.main_layout.addWidget(self.left_widget, 0, 0, 16, 3)
        self.main_layout.addWidget(self.right_widget, 0, 3, 16, 11)
        self.setCentralWidget(self.main_widget)

        self.left_label_pohoto = QtWidgets.QToolButton()
        self.left_label_pohoto.setIcon(QtGui.QIcon(QtGui.QPixmap("../头像.png")))
        self.left_label_pohoto.setIconSize(QtCore.QSize(300, 300))
        self.left_label_pohoto.setObjectName("left_label_photo")

        self.left_label1 = QtWidgets.QLabel("昵称：")
        self.left_label1.setObjectName("left_label")
        self.left_label2 = QtWidgets.QLabel("性别：")
        self.left_label2.setObjectName("left_label")
        self.left_label3 = QtWidgets.QLabel("等级：")
        self.left_label3.setObjectName("left_label")
        self.left_label4 = QtWidgets.QLabel("简介：")
        self.left_label4.setObjectName("left_label")
        self.left_label1.setOpenExternalLinks(True)  # 允许访问超链接
        self.left_label1.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.left_label1.linkActivated.connect(self.link_clicked)  # 针对链接点击事件

        self.combox = QtWidgets.QComboBox()
        self.combox.addItems(["今日新人", "ItemCF", "UserCF", "Tags","隐语义"])
        # select_value = self.comboBox.currentText() --> 使用currentText()函数获取下拉框中选择的值
        self.btn_choose = QtWidgets.QPushButton("确认")
        self.btn_choose.setObjectName("button")
        self.btn_choose.clicked.connect(lambda: self.recommend())

        self.uid_input = QtWidgets.QLineEdit()
        self.uid_input.setPlaceholderText("输入你的uid号")
        self.btn_uid = QtWidgets.QPushButton("确认")
        self.btn_uid.setObjectName("button")
        self.btn_uid.clicked.connect(lambda: self.send_uid())

        self.left_layout.addWidget(self.btn_uid, 0, 1, 1, 1)
        self.left_layout.addWidget(self.uid_input, 0, 0, 1, 1)
        self.left_layout.addWidget(self.combox, 1, 0, 1, 1)
        self.left_layout.addWidget(self.btn_choose, 1, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_pohoto, 2, 0, 3, 2)
        self.left_layout.addWidget(self.left_label1, 5, 0, 1, 2)
        self.left_layout.addWidget(self.left_label2, 6, 0, 1, 2)
        self.left_layout.addWidget(self.left_label3, 7, 0, 1, 2)
        self.left_layout.addWidget(self.left_label4, 8, 0, 1, 2)

        # 插入新人up
        self.right_label = QtWidgets.QLabel("今日新人TOP5")
        self.right_label.setObjectName("right_label")
        pixmap = QtGui.QPixmap("../热门.png")
        self.top_label = QtWidgets.QToolButton()
        self.top_label.setIcon(QtGui.QIcon(pixmap))
        self.top_label.setIconSize(QtCore.QSize(60, 55))

        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐新人
        self.right_commend_layout = QtWidgets.QGridLayout()
        self.right_recommend_widget.setLayout(self.right_commend_layout)

        self.right_new1 = QtWidgets.QWidget()
        self.right_new1_layout = QtWidgets.QGridLayout()
        self.right_new1.setLayout(self.right_new1_layout)
        self.right_new1.setObjectName("right_widget")

        self.right_new2 = QtWidgets.QWidget()
        self.right_new2_layout = QtWidgets.QGridLayout()
        self.right_new2.setLayout(self.right_new2_layout)
        self.right_new2.setObjectName("right_widget")

        self.right_new3 = QtWidgets.QWidget()
        self.right_new3_layout = QtWidgets.QGridLayout()
        self.right_new3.setLayout(self.right_new3_layout)
        self.right_new3.setObjectName("right_widget")

        self.right_new4 = QtWidgets.QWidget()
        self.right_new4_layout = QtWidgets.QGridLayout()
        self.right_new4.setLayout(self.right_new4_layout)
        self.right_new4.setObjectName("right_widget")

        self.right_new5 = QtWidgets.QWidget()
        self.right_new5_layout = QtWidgets.QGridLayout()
        self.right_new5.setLayout(self.right_new5_layout)
        self.right_new5.setObjectName("right_widget")

        self.right_layout.addWidget(self.right_label, 0, 1, 1, 11)
        self.right_layout.addWidget(self.top_label, 0, 0, 1, 1)
        self.right_layout.addWidget(self.right_new1, 1, 0, 3, 11)
        self.right_layout.addWidget(self.right_new2, 4, 0, 3, 11)
        self.right_layout.addWidget(self.right_new3, 7, 0, 3, 11)
        self.right_layout.addWidget(self.right_new4, 10, 0, 3, 11)
        self.right_layout.addWidget(self.right_new5, 13, 0, 3, 11)

        rookie_list = rookie_info()
        # r_info.append([line['owner']['mid'], line['owner']['name'], line['owner']['face'], line['title'],line['short_link'],line['pic']])

        res_pic1 = requests.get(rookie_list[0][5])
        img1 = QtGui.QImage.fromData(res_pic1.content)
        self.right_new1_label1 = QtWidgets.QToolButton()
        self.right_new1_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img1)))
        self.right_new1_label1.setIconSize(QtCore.QSize(150, 100))

        self.right_new1_label2 = QtWidgets.QLabel("标题：" + "<a href='" + str(rookie_list[0][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            rookie_list[0][3]) + "</a>")
        self.right_new1_label2.setOpenExternalLinks(True)  # 允许访问超链接
        self.right_new1_label2.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.right_new1_label2.linkActivated.connect(self.link_clicked)  # 针对链接点击事件
        self.right_new1_label3 = QtWidgets.QLabel(
            "昵称:" + str(rookie_list[0][1]) + "  " + "uid:" + str(rookie_list[0][0]))
        self.right_new1_label2.setWordWrap(True)
        # self.btn_uid.clicked.connect(lambda: self.send_uid())

        self.right_new1_layout.addWidget(self.right_new1_label1, 0, 0, 3, 2)
        self.right_new1_layout.addWidget(self.right_new1_label2, 0, 2, 2, 9)
        self.right_new1_layout.addWidget(self.right_new1_label3, 2, 2, 1, 9)

        res_pic2 = requests.get(rookie_list[1][5])
        img2 = QtGui.QImage.fromData(res_pic2.content)
        self.right_new2_label1 = QtWidgets.QToolButton()
        self.right_new2_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img2)))
        self.right_new2_label1.setIconSize(QtCore.QSize(150, 100))
        self.right_new2_label2 = QtWidgets.QLabel("标题：" + "<a href='" + str(rookie_list[1][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            rookie_list[1][3]) + "</a>")
        self.right_new2_label2.setOpenExternalLinks(True)  # 允许访问超链接
        self.right_new2_label2.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.right_new2_label2.linkActivated.connect(self.link_clicked)  # 针对链接点击事件
        self.right_new2_label3 = QtWidgets.QLabel(
            "昵称:" + str(rookie_list[1][1]) + "  " + "uid:" + str(rookie_list[1][0]))
        self.right_new2_label2.setWordWrap(True)

        self.right_new2_layout.addWidget(self.right_new2_label1, 0, 0, 3, 2)
        self.right_new2_layout.addWidget(self.right_new2_label2, 0, 2, 2, 9)
        self.right_new2_layout.addWidget(self.right_new2_label3, 2, 2, 1, 9)

        res_pic3 = requests.get(rookie_list[2][5])
        img3 = QtGui.QImage.fromData(res_pic3.content)
        self.right_new3_label1 = QtWidgets.QToolButton()
        self.right_new3_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img3)))
        self.right_new3_label1.setIconSize(QtCore.QSize(150, 100))
        self.right_new3_label2 = QtWidgets.QLabel("标题：" + "<a href='" + str(rookie_list[2][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            rookie_list[2][3]) + "</a>")
        self.right_new3_label2.setOpenExternalLinks(True)  # 允许访问超链接
        self.right_new3_label2.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.right_new3_label2.linkActivated.connect(self.link_clicked)  # 针对链接点击事件
        self.right_new3_label3 = QtWidgets.QLabel(
            "昵称:" + str(rookie_list[2][1]) + "  " + "uid:" + str(rookie_list[2][0]))
        self.right_new3_label2.setWordWrap(True)

        self.right_new3_layout.addWidget(self.right_new3_label1, 0, 0, 3, 2)
        self.right_new3_layout.addWidget(self.right_new3_label2, 0, 2, 2, 9)
        self.right_new3_layout.addWidget(self.right_new3_label3, 2, 2, 1, 9)

        res_pic4 = requests.get(rookie_list[3][5])
        img4 = QtGui.QImage.fromData(res_pic4.content)
        self.right_new4_label1 = QtWidgets.QToolButton()
        self.right_new4_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img4)))
        self.right_new4_label1.setIconSize(QtCore.QSize(150, 100))
        self.right_new4_label2 = QtWidgets.QLabel("标题：" + "<a href='" + str(rookie_list[3][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            rookie_list[3][3]) + "</a>")
        self.right_new4_label2.setOpenExternalLinks(True)  # 允许访问超链接
        self.right_new4_label2.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.right_new4_label2.linkActivated.connect(self.link_clicked)  # 针对链接点击事件
        self.right_new4_label3 = QtWidgets.QLabel(
            "昵称:" + str(rookie_list[3][1]) + "  " + "uid:" + str(rookie_list[3][0]))
        self.right_new4_label2.setWordWrap(True)

        self.right_new4_layout.addWidget(self.right_new4_label1, 0, 0, 3, 2)
        self.right_new4_layout.addWidget(self.right_new4_label2, 0, 2, 2, 9)
        self.right_new4_layout.addWidget(self.right_new4_label3, 2, 2, 1, 9)

        res_pic5 = requests.get(rookie_list[4][5])
        img5 = QtGui.QImage.fromData(res_pic5.content)
        self.right_new5_label1 = QtWidgets.QToolButton()
        self.right_new5_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img5)))
        self.right_new5_label1.setIconSize(QtCore.QSize(150, 100))
        self.right_new5_label2 = QtWidgets.QLabel("标题：" + "<a href='" + str(rookie_list[4][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            rookie_list[4][3]) + "</a>")
        self.right_new5_label2.setOpenExternalLinks(True)  # 允许访问超链接
        self.right_new5_label2.linkHovered.connect(self.link_hovered)  # 针对链接光标略过
        self.right_new5_label2.linkActivated.connect(self.link_clicked)  # 针对链接点击事件
        self.right_new5_label3 = QtWidgets.QLabel(
            "昵称:" + str(rookie_list[4][1]) + "  " + "uid:" + str(rookie_list[4][0]))
        self.right_new5_label2.setWordWrap(True)

        self.right_new5_layout.addWidget(self.right_new5_label1, 0, 0, 3, 2)
        self.right_new5_layout.addWidget(self.right_new5_label2, 0, 2, 2, 9)
        self.right_new5_layout.addWidget(self.right_new5_label3, 2, 2, 1, 9)

        # self.left_layout.addWidget(self.btn, 1, 0, 1, 3)
        # QList<QPushButton*> btns = ui->scrollAreaWidgetContents->findChildren<QPushButton*>();
        # foreach (QPushButton* btn, btns) {   delete btn;  }

        # 美化工作
        self.uid_input.setStyleSheet(
            '''
            QLineEdit{
            font-family:"方正清刻本悦宋简体";
            font:8pt;
            border:1px solid black;
            border-radius:10px;
            padding:2px 4px;
            }
            '''
        )
        self.right_widget.setStyleSheet(
            '''
            QWidget#right_widget{
            color:#232C51;
            background:#FFFFFF;
            border-bottom:1px solid darkGray;
            }
            
            
            '''
        )
        self.left_widget.setStyleSheet(
            '''
            QPushButton{ background: #00A1D6;
                         color: white;
                         border-radius:2px;
                          width: 75px;
                          height: 28px;
                         }
            QPushButton:hover
            {
             background: #00B1E2;
             color: white;
            }
            QLabel#left_label{
            font: 10pt;
            font-family:"方正清刻本悦宋简体";
            color: black;
            }
            

            '''
        )
        self.combox.setStyleSheet(
            '''
            QComboBox{
            border: 1px solid gray;
            border-radius: 4px;
            font-family:"宋体";
            height:30px;
            font:10pt;

            }
            QComboBox QAbstractItemView{
             border: 3px solid darkgray;
             selection-background-color: darkGray;}
            QComboBox::drop-down {border:0px solid gray;width: 40px;}

            '''
        )
        self.top_label.setStyleSheet(
            '''
            QToolButton{
            border:none;
            border_bottom:5px ;
            border_left:3px ;
            border_right:2px ;
            }
            '''
        )
        self.right_label.setStyleSheet(
            '''
            QLabel{
            font-family:"方正清刻本悦宋简体";
            font:20pt;
            color:#404040;
            }
            '''
        )

        self.right_new1.setStyleSheet(
            '''
         QToolButton{border:none;}
         QToolButton:hover{border_bottom:2px solid #F76677;}
         QLabel{
         font:9pt;
         font-family:"宋体";
         }

        '''
        )
        self.right_new2.setStyleSheet(
            '''
         QToolButton{border:none;}
         QToolButton:hover{border_bottom:2px solid #F76677}
         QLabel{
         font:9pt;
         font-family:"宋体";
         }

        '''
        )
        self.right_new3.setStyleSheet(
            '''
         QToolButton{border:none;}
         QToolButton:hover{border_bottom:2px solid #F76677}
         QLabel{
         font:9pt;
         font-family:"宋体";
         }

        '''
        )
        self.right_new4.setStyleSheet(
            '''
         QToolButton{border:none;}
         QToolButton:hover{border_bottom:2px solid #F76677}
         QLabel{
         font:9pt;
         font-family:"宋体";
         }

        '''
        )
        self.right_new5.setStyleSheet(
            '''
         QToolButton{border:none;}
         QToolButton:hover{border_bottom:2px solid #F76677}
         QLabel{
         font:9pt;
         font-family:"宋体";
         }

        '''
        )
        self.left_label_pohoto.setStyleSheet(
            '''
            QToolButton{border:none;}
            QToolButton:hover{border_bottom:2px solid #F76677}

            '''
        )

        self.main_layout.setSpacing(0)

    def recommend(self):
        '''
        选择推荐算法后在此函数中进行up主推荐
        '''
        uid=int(self.uid_input.text())
        if uid==None:
            self.messageDialog_warn()
            return

        rem_algorithm = self.combox.currentText()
        if rem_algorithm == "今日新人":
            print("推荐今日新人")
            self.right_label.setText("今日新人TOP5")
            recommend_list = rookie_info()
            return recommend_list
            self.recommend_rookie(recommend_list)
            return


        elif rem_algorithm == "ItemCF":
            print("基于物品的协同推荐")
            list_up = recommend_4.recommend_IC(uid)
            print(list_up)
            if list_up:
                list_recom = get_list_recommend(uid, list_up)
                print(list_recom)
                self.right_label.setText("UP主推荐TOP5")
                self.recommend_rookie(list_recom)
                return
            else:
                self.messageDialog()
                return

        elif rem_algorithm == "UserCF":
            print("基于用户的协同推荐")
            self.right_label.setText("UP主推荐TOP5")
            list_up = recommend_4.recommend_UC(uid)
            print(list_up)
            if list_up:
                list_recom = get_list_recommend(uid, list_up)
                print(list_recom)
                self.right_label.setText("UP主推荐TOP5")
                self.recommend_rookie(list_recom)
                return
            else:
                self.messageDialog()
                return
        elif rem_algorithm=="Tags":
            print("基于标签的推荐")
            self.right_label.setText("UP主推荐TOP5")
            list_up = recommend_4.recommend_Tags(uid)
            print(list_up)
            if list_up:
                list_recom = get_list_recommend(uid, list_up)
                print(list_recom)
                self.right_label.setText("UP主推荐TOP5")
                self.recommend_rookie(list_recom)
                return
            else:
                self.messageDialog()
                return
        else:
            print("隐语义推荐")
            self.right_label.setText("UP主推荐TOP5")
            list_up = recommend_4.recommend_Hidden(uid)
            print(list_up)
            if list_up:
                list_recom = get_list_recommend(uid, list_up)
                print(list_recom)
                self.right_label.setText("UP主推荐TOP5")
                self.recommend_rookie(list_recom)
                return
            else:
                self.messageDialog()
                return

    def send_uid(self):
        uid = self.uid_input.text()
        if uid.isdigit():
            uid = int(uid)

            user_info = func_user_info(int(uid))
        else:
            self.buhefa()
            return
            # 写个警告！！！
        res = requests.get(user_info['face'])
        img = QtGui.QImage.fromData(res.content)
        self.left_label_pohoto.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img)))
        # https://space.bilibili.com/297197546
        self.left_label1.setText("昵称：<a href='https://space.bilibili.com/" + str(uid) + "'style='color:black'>" +
                                 str(user_info["name"]) + "</a>")
        self.left_label2.setText("性别：" + str(user_info["性别"]))
        self.left_label3.setText("等级：" + str(user_info["等级"]))
        self.left_label4.setText("简介：" + str(user_info["简介"]))
        # https://blog.csdn.net/qq_36591505/article/details/104657198

    def link_hovered(self):
        return

    def link_clicked(self):
        print("点击时触发事件")

    def messageDialog(self):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '对不起！', '我们的数据库还没有覆盖到您')
        msg_box.exec_()
    def messageDialog_warn(self):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '警告！', '您还没有输入用户uid')
        msg_box.exec_()
    def buhefa(self):
        msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '警告！', '您输入的uid有误，请核对后再次输入')
        msg_box.exec_()

    def recommend_rookie(self,recommend_list):
        res_pic1 = requests.get(recommend_list[0][5])
        img1 = QtGui.QImage.fromData(res_pic1.content)
        self.right_new1_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img1)))
        self.right_new1_label2.setText("标题：" + "<a href='" + str(recommend_list[0][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            recommend_list[0][3]) + "</a>")
        print(recommend_list[0][3])
        self.right_new1_label3.setText(
            "昵称:" + str(recommend_list[0][1]) + "  " + "uid:" + str(recommend_list[0][0])+"  "+"评分："+str(recommend_list[0][2]))

        res_pic2 = requests.get(recommend_list[1][5])
        img2 = QtGui.QImage.fromData(res_pic2.content)
        self.right_new2_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img2)))
        self.right_new2_label2.setText("标题：" + "<a href='" + str(recommend_list[1][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            recommend_list[1][3]) + "</a>")
        self.right_new2_label3.setText(
            "昵称:" + str(recommend_list[1][1]) + "  " + "uid:" + str(recommend_list[1][0])+"  "+"评分："+str(recommend_list[1][2]))

        res_pic3 = requests.get(recommend_list[2][5])
        img3 = QtGui.QImage.fromData(res_pic3.content)
        self.right_new3_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img3)))
        self.right_new3_label2 .setText("标题：" + "<a href='" + str(recommend_list[2][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            recommend_list[2][3]) + "</a>")
        self.right_new3_label3 .setText(
            "昵称:" + str(recommend_list[2][1]) + "  " + "uid:" + str(recommend_list[2][0])+"  "+"评分："+str(recommend_list[2][2]))

        res_pic4 = requests.get(recommend_list[3][5])
        img4 = QtGui.QImage.fromData(res_pic4.content)
        self.right_new4_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img4)))
        self.right_new4_label2 .setText("标题：" + "<a href='" + str(recommend_list[3][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            recommend_list[3][3]) + "</a>")
        self.right_new4_label3 .setText(
            "昵称:" + str(recommend_list[3][1]) + "  " + "uid:" + str(recommend_list[3][0])+"  "+"评分："+str(recommend_list[3][2]))

        res_pic5 = requests.get(recommend_list[4][5])
        img5 = QtGui.QImage.fromData(res_pic5.content)
        self.right_new5_label1.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(img5)))
        self.right_new5_label2.setText("标题：" + "<a href='" + str(recommend_list[4][4]) +
                                                  "' style='text-decoration:none;color:black'>" + str(
            recommend_list[4][3]) + "</a>")
        self.right_new5_label3 .setText(
            "昵称:" + str(recommend_list[4][1]) + "  " + "uid:" + str(recommend_list[4][0])+"  "+"评分："+str(recommend_list[4][2]))


def func_user_info(mid):
    url_user = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(mid)
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    head = {'user-agent': useragent}
    user_info = requests.get(url_user, headers=head)
    f = user_info.json()
    print(f)
    user_name = f['data']['name']
    user_sex = f['data']['sex']
    user_face = f['data']['face']  # 后续做前端可能会用到
    user_sign = f['data']['sign']
    user_level = f['data']['level']
    print(user_name, "性别：" + user_sex, str(user_level) + '级号', "简介：" + user_sign, sep='\n')
    if len(user_sign) <= 12:
        info = {"face": user_face, "name": user_name, "性别": user_sex, "等级": str(user_level), "简介": user_sign}
    else:
        info = {"face": user_face, "name": user_name, "性别": user_sex, "等级": str(user_level), "简介": user_sign[:12] + "…"}

    return info
def rookie_info():
    '''
    获得今日新人top5的信息
    :return: r_info
    '''
    url_rookie = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie"
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    head = {'user-agent': useragent}
    r_rookie = requests.get(url_rookie, headers=head)
    rookie_info = r_rookie.json()
    # print(rookie_info)
    rr = rookie_info['data']['list']
    r_info = []
    count = 0
    for line in rr:
        # description_rookie = str(jieba.analyse.textrank(line['desc'])).replace(',', ' ')
        r_info.append(
            [line['owner']['mid'], line['owner']['name'], line['owner']['face'], line['title'], line['short_link'],
             line['pic']])
        # print(line['short_link'])
        count = count + 1
        if count >= 5:
            break
    return r_info
def get_list_recommend(uid,list_up):
    recom_info = []
    sum=0
    for l in list_up:
        sum=sum+l[1]

    for l in list_up:
        if int(l[0])==int(uid):
            continue
        r_video = bilibili_api.user.get_videos(int(l[0]))
        wangzhi = "https://www.bilibili.com/video/"
        if r_video:
            recom_info.append(
                [l[0], r_video[0]['author'], l[1]/sum, r_video[0]['title'], wangzhi + str(r_video[0]['bvid']),r_video[0]['pic'] ])
        else:
            url_user = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(l[0])
            useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                        'Safari/537.36 '
            head = {'user-agent': useragent}
            user_info = requests.get(url_user, headers=head)
            f = user_info.json()
            # print(f)
            user_name = f['data']['name']
            user_face = f['data']['face']
            wangzhi2="https://space.bilibili.com/"

            recom_info.append([l[0], user_name, l[1]/sum, "他还没有发布过视频哦", wangzhi2+str(l[0]),user_face])
    #print(recom_info)
    return recom_info
def main():
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('../吕老师撅嘴.png'))
    splash.show()
    # 可以显示启动信息
    gui = main_ui()
    gui.setObjectName("main_window")
    gui.setStyleSheet("#main_window{background-color:#FFFFFF}")
    # 关闭启动画面
    splash.close()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # rookie_info()
