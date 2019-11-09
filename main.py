# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : main.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019/11/6 下午 11:05
#   desc     : 
# =====================================================

import sqlite3

from PyQt5.QtGui import QFont
from PyQt5 import QtGui

import mysql
import bills

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from ui import consume_ui, update_log_ui, add_person_ui, main_ui

import os
import time
import webbrowser
import requests

COST_1 = 10
COST_2 = 10
COST_3 = 30
COST_4 = 20
COLUMN = 7


class MainWindow(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.init_sign()
        self.init_view()

        if not os.path.exists('data.db'):
            mysql.init_database()
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

        self.sort_enable = False
        self.load_initial_data()
        self.load_initial_bill()

    def init_sign(self):
        self.pushButton_2.clicked.connect(self.add_person)
        self.pushButton_5.clicked.connect(self.search)
        self.pushButton_3.clicked.connect(self.invest)
        self.pushButton_6.clicked.connect(self.load_initial_data)
        self.pushButton_4.clicked.connect(self.consume)
        self.pushButton.clicked.connect(self.del_person)
        self.tabWidget.currentChanged.connect(self.change_tab)
        self.tableWidget_2.horizontalHeader().sectionClicked.connect(self.sort_row)
        self.action1.triggered.connect(self.update_log)
        self.action_2.triggered.connect(self.about)
        self.action_3.triggered.connect(self.update_me)
        self.lineEdit.returnPressed.connect(self.search)
        self.action_4.triggered.connect(lambda: webbrowser.open('https://skycity233.github.io/DataManager/'))

    def init_view(self):

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        self.tableWidget.customContextMenuRequested.connect(self.generate_menu)  # 右键菜单 消费设置
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能一行
        self.tableWidget.verticalHeader().setVisible(False)  # 不显示行号
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只能一行
        self.tableWidget_2.verticalHeader().setVisible(False)  # 不显示行号
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def invest(self):
        index = self.tableWidget.currentRow()
        if index < 0:
            QMessageBox.information(self, "温馨提示", "请先选择充值的账户", QMessageBox.Yes)
            return
        value, ok = QInputDialog.getInt(self, "正在充值", "请输入充值金额:", 0, 0, 10000, 10)
        if ok:
            reply = QMessageBox.information(self, "充值确认",
                                            "正在给" + self.tableWidget.item(index, 1).text() + "充值" + str(
                                                value) + '元，是否充值',
                                            QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                person = mysql.query('user_tb', '_id', self.tableWidget.item(index, 0).text())
                balance = float(person[0][4]) + value
                mysql.change(self.tableWidget.item(index, 0).text(), 'balance', str(balance))
                QMessageBox.information(self, "温馨提示", "充值成功", QMessageBox.Yes)

                bills.bill_in(str(value), person[0][1], person[0][2], person[0][3])
                self.load_initial_data()
                self.load_initial_bill()

    def consume(self):
        index = self.tableWidget.currentRow()
        if index < 0:
            QMessageBox.information(self, "温馨提示", "请先选择要消费的会员", QMessageBox.Yes)
            return
        ConsumeWindow.name = self.tableWidget.item(index, 1).text()
        ConsumeWindow.id = self.tableWidget.item(index, 0).text()
        ConsumeWindow.show()

    def add_person(self):
        AddWindow.show()

    def del_person(self):
        index = self.tableWidget.currentRow()
        if index < 0:
            QMessageBox.information(self, "温馨提示", "请先选择要删除的账户，可按Ctrl多选", QMessageBox.Yes)
            return
        items = self.tableWidget.selectedItems()
        reply = QMessageBox.information(self, "提示", "确定删除已选中的会员？", QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            for i in range(int((len(items) + 1) / COLUMN)):
                mysql.del_person(items[2 + i * 7].text())
            MainWindow.load_initial_data()

    def search(self):
        line = self.lineEdit.text()
        if not line:
            QMessageBox.information(self, "温馨提示", "请输入手机号或卡号", QMessageBox.Yes)
            return

        if len(line) == 11:
            type = 'phone'
        else:
            type = 'card'

        id = mysql.query('user_tb', type, line)
        if not id:
            QMessageBox.information(self, "温馨提示", "未能找到对应的手机号或卡号", QMessageBox.Yes)
        else:
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.removeRow(0)
            for row in id:
                inx = id.index(row)
                self.tableWidget.insertRow(inx)
                for i in range(len(row)):
                    item = QTableWidgetItem(str(row[i]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 无法编辑
                    self.tableWidget.setItem(inx, i, item)

    def search_bill(self, text=None):
        line = self.lineEdit.text()
        if text:
            line = text
        if not line:
            QMessageBox.information(self, "温馨提示", "请输入手机号或卡号", QMessageBox.Yes)
            return

        if len(line) == 11:
            type = 'phone'
        else:
            type = 'card'

        id = mysql.query('bill_tb', type, line)
        if not id:
            QMessageBox.information(self, "温馨提示", "未能找到对应的手机号或卡号", QMessageBox.Yes)
        else:
            for i in range(self.tableWidget_2.rowCount()):
                self.tableWidget_2.removeRow(0)
            for row in id:
                inx = id.index(row)
                self.tableWidget_2.insertRow(inx)
                for i in range(len(row)):
                    item = QTableWidgetItem(str(row[i]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 无法编辑
                    self.tableWidget_2.setItem(inx, i, item)

    def load_initial_data(self):

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)

        self.c.execute('''SELECT * FROM user_tb ''')
        rows = self.c.fetchall()

        for row in rows:
            inx = rows.index(row)
            self.tableWidget.insertRow(inx)
            for i in range(7):
                item = QTableWidgetItem(str(row[i]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 无法编辑
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(inx, i, item)

    def load_initial_bill(self):

        for i in range(self.tableWidget_2.rowCount()):
            self.tableWidget_2.removeRow(0)

        self.c.execute('''SELECT * FROM bill_tb ''')
        rows = self.c.fetchall()

        for row in rows:
            inx = rows.index(row)
            self.tableWidget_2.insertRow(inx)
            for i in range(8):

                item = QTableWidgetItem()
                if str(row[i]).isdigit:  # 使得数字排序能够正常的运行
                    item.setData(Qt.DisplayRole, row[i])
                else:
                    item.setText(row[i])

                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 无法编辑
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_2.setItem(inx, i, item)
                del item

        self.tableWidget_2.sortItems(1, Qt.DescendingOrder)

    def generate_menu(self, pos):

        row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num >= 0:
            menu = QMenu()
            item1 = menu.addAction(u"修改信息")
            item2 = menu.addAction(u"查看流水")
            item3 = menu.addAction(u"删除")

            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item1:
                DetailWindow.name = self.tableWidget.item(row_num, 1).text()
                DetailWindow.phone = self.tableWidget.item(row_num, 2).text()
                DetailWindow.card = self.tableWidget.item(row_num, 3).text()
                DetailWindow.gender = self.tableWidget.item(row_num, 5).text()
                DetailWindow.birth = self.tableWidget.item(row_num, 6).text()
                DetailWindow.note = ' ' or self.tableWidget.item(row_num, 7).text()
                DetailWindow.change()
                DetailWindow.show()

            elif action == item2:
                self.search_bill(self.tableWidget.item(row_num, 2).text())
                self.tabWidget.setCurrentIndex(1)  # 切换界面

            elif action == item3:
                if float(self.tableWidget.item(row_num, 4).text()) == 0:
                    reply = QMessageBox.information(self, "提示", "确定删除？", QMessageBox.Yes | QMessageBox.No)
                    if reply == 16384:
                        mysql.del_person(self.tableWidget.item(row_num, 2).text())
                    MainWindow.load_initial_data()
                else:
                    reply = QMessageBox.information(self, "提示", "检测到此会员尚有余额，删除会将余额清零，是否继续？",
                                                    QMessageBox.Yes | QMessageBox.No)
                    if reply == 16384:
                        mysql.del_person(self.tableWidget.item(row_num, 2).text())
                        bills.bill_out(str(float(self.tableWidget.item(row_num, 4).text())),
                                       self.tableWidget.item(row_num, 1).text(),
                                       self.tableWidget.item(row_num, 2).text(),
                                       self.tableWidget.item(row_num, 3).text())
                    MainWindow.load_initial_data()
            else:
                return

    def sort_row(self, index):
        if not self.sort_enable:
            self.tableWidget_2.sortItems(index, Qt.AscendingOrder)
            self.sort_enable = True
        else:
            self.tableWidget_2.sortItems(index, Qt.DescendingOrder)
            self.sort_enable = False

    def update_log(self):
        UpdateWindow.show()

    def update_me(self):

        api = 'https://api.github.com/repos/skycity233/DataManager'
        all_page = requests.get(api).json()  # 获取api页面(此时是以json返回的页面)并将该页面转换成字典形式（key-value的存储方式）
        cur_update = all_page['updated_at']
        last_update = '2019-11-09T05:57:11Z'
        if cur_update != last_update:
            QMessageBox.information(self, "提示", "检查到更新")
        else:
            QMessageBox.information(self, "提示", "未检查到更新")

    def about(self):
        QMessageBox.information(self, "关于", "作者：王保键\n版本：v1.1.0\n更新日期：2019-11-8", QMessageBox.Yes)

    def change_tab(self):
        if self.tabWidget.currentIndex() == 0:
            self.pushButton.setVisible(True)
            self.pushButton_2.setVisible(True)
            self.pushButton_3.setVisible(True)
            self.pushButton_4.setVisible(True)
            self.pushButton_5.setText('搜索会员')
            try:
                self.pushButton_5.clicked.connect(self.search)
                self.pushButton_5.clicked.disconnect(self.search_bill)
                self.lineEdit.returnPressed.connect(self.search)
                self.lineEdit.returnPressed.disconnect(self.search_bill)
                self.pushButton_6.clicked.connect(self.load_initial_data)
                self.pushButton_6.clicked.disconnect(self.load_initial_bill)
            except:
                pass
        elif self.tabWidget.currentIndex() == 1:
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(False)
            self.pushButton_3.setVisible(False)
            self.pushButton_4.setVisible(False)
            self.pushButton_5.setText('搜索流水')
            try:
                self.pushButton_5.clicked.connect(self.search_bill)
                self.pushButton_5.clicked.disconnect(self.search)
                self.lineEdit.returnPressed.connect(self.search_bill)
                self.lineEdit.returnPressed.disconnect(self.search)
                self.pushButton_6.clicked.connect(self.load_initial_bill)
                self.pushButton_6.clicked.disconnect(self.load_initial_data)
            except:
                pass
        elif self.tabWidget.currentIndex() == 2:
            self.tabWidget.setCurrentIndex(0)
            QMessageBox.information(self, "温馨提示", "暂不支持", QMessageBox.Yes)


class AddWindow(QDialog, add_person_ui.Ui_Form):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.init_sign()

    def init_sign(self):
        self.pushButton.clicked.connect(self.add_person)

    def add_person(self):
        name = self.lineEdit.text()
        phone = self.lineEdit_1.text()
        card = self.lineEdit_2.text()
        balance = self.doubleSpinBox.text()
        gender = self.comboBox.currentText()
        birth = self.dateEdit.text()
        note = self.lineEdit_3.text()

        if len(phone) != 11:
            QMessageBox.information(self, "温馨提示", "手机号格式不正确。", QMessageBox.Yes)
            return
        if mysql.query('user_tb', 'phone', phone):
            QMessageBox.information(self, "温馨提示", "手机号已存在。", QMessageBox.Yes)
            return
        if mysql.query('user_tb', 'card', card):
            QMessageBox.information(self, "温馨提示", "卡号已存在。", QMessageBox.Yes)
            return
        else:
            mysql.add_person(name, phone, card, balance, gender, birth, note)
            bills.bill_in(str(balance), name, phone, card)
            AddWindow.close()
            MainWindow.load_initial_data()

        return


class DetailWindow(QDialog, add_person_ui.Ui_Form):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.init_sign()
        self.setWindowTitle('修改信息')
        self.doubleSpinBox.setEnabled(False)
        self.dateEdit.setEnabled(False)

    def init_sign(self):
        self.pushButton.clicked.connect(self.add_person)

    def change(self):
        self.lineEdit.setText(DetailWindow.name)
        self.lineEdit_1.setText(DetailWindow.phone)
        self.lineEdit_2.setText(DetailWindow.card)
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_3.setText(DetailWindow.note)

    def add_person(self):

        name = self.lineEdit.text()
        phone = self.lineEdit_1.text()
        card = self.lineEdit_2.text()
        balance = self.doubleSpinBox.text()
        gender = self.comboBox.currentText()
        birth = self.dateEdit.text()
        note = self.lineEdit_3.text()

        if len(phone) != 11:
            QMessageBox.information(self, "温馨提示", "手机号格式不正确。", QMessageBox.Yes)
            return
        if mysql.query('user_tb', 'phone', phone) and phone != DetailWindow.phone:
            QMessageBox.information(self, "温馨提示", "手机号已存在。", QMessageBox.Yes)
            return
        if mysql.query('user_tb', 'card', card) and card != DetailWindow.card:
            QMessageBox.information(self, "温馨提示", "卡号已存在。", QMessageBox.Yes)
            return
        else:

            DetailWindow.close()
            MainWindow.load_initial_data()
        QMessageBox.information(self, "温馨提示", "修改失败，此功能待完善。", QMessageBox.Yes)
        return


# class DetailWindow(QDialog, detail_ui.Ui_Form):
#     def __init__(self):
#         QDialog.__init__(self)
#         self.setupUi(self)


class ConsumeWindow(QDialog, consume_ui.Ui_Form):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.checkBox.clicked.connect(self.check_checkbox)
        self.checkBox_2.clicked.connect(self.check_checkbox)
        self.checkBox_3.clicked.connect(self.check_checkbox)
        self.checkBox_4.clicked.connect(self.check_checkbox)
        self.pushButton.clicked.connect(self.submit)

    def check_checkbox(self):
        self.cost = 0
        if self.checkBox.checkState():
            self.cost += COST_1
        if self.checkBox_2.checkState():
            self.cost += COST_2
        if self.checkBox_3.checkState():
            self.cost += COST_3
        if self.checkBox_4.checkState():
            self.cost += COST_4
        self.label.setText('总金额：' + str(self.cost) + '，SVIP优惠价格：' + str(self.cost * 0.75))

    def submit(self):

        reply = QMessageBox.information(self, "消费确认",
                                        self.name + "消费" + str(self.cost) + '元？', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            person = mysql.query('user_tb', '_id', self.id)
            balance = float(person[0][4]) - self.cost
            if balance < 0:
                QMessageBox.information(self, "温馨提示", "余额不足，请充值", QMessageBox.Yes)
            else:
                mysql.change(self.id, 'balance', str(balance))
                QMessageBox.information(self, "温馨提示", "消费成功", QMessageBox.Yes)

                bills.bill_out(str(self.cost), str(person[0][1]), str(person[0][2]), str(person[0][3]))
                MainWindow.load_initial_data()
                MainWindow.load_initial_bill()
        self.close()


class UpdateWindow(QDialog, update_log_ui.Ui_Form):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)


def show_loading(vip):
    # 其实这个加载动画是假的，但是挺好看的，谁知道呢，哈哈哈哈

    # 创建QSplashScreen对象实例
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("data.png"))
    # 设置画面中的文字的字体
    splash.setFont(QFont('Microsoft YaHei UI', 10))
    # 显示画面
    splash.show()
    # 显示信息
    splash.showMessage("启动中", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

    if not vip:
        for i in range(7):
            time.sleep(0.1)
            splash.showMessage("正在加载样式表..." + str(i * 2) + "%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
                               QtCore.Qt.white)
        time.sleep(1)
        for i in range(13):
            time.sleep(0.1)
            splash.showMessage("正在加载样式表..." + str(12 + i * 2) + "%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
                               QtCore.Qt.white)
        for i in range(10):
            time.sleep(0.1)
            splash.showMessage("正在加载数据库..." + str(40 + i * 2) + "%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
                               QtCore.Qt.white)
        time.sleep(0.5)
        for i in range(20):
            time.sleep(0.1)
            splash.showMessage("正在测试数据库..." + str(58 + i * 2) + "%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
                               QtCore.Qt.white)

        splash.showMessage("正在测试数据库...99%", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        time.sleep(2)

    splash.finish(MainWindow)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    AddWindow = AddWindow()
    DetailWindow = DetailWindow()
    UpdateWindow = UpdateWindow()
    ConsumeWindow = ConsumeWindow()
    show_loading(vip=True)  # 显示启动加载页面
    MainWindow.show()  # 当主界面显示后销毁启动画面
    sys.exit(app.exec_())
