# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v2.0.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cgitb

cgitb.enable()


def calclt(n, ap, bp, cp, wqd):
    # 处理电压源
    ptn = []  # 存储有伴电压源的结点对
    nptn = []  # 存储无伴电压源的结点对
    for i in range(0, n):
        for j in range(i + 1, n):
            v = float(cp[i][j])
            if v > 0 or v < 0:
                if (i, j) in wqd:
                    nptn.append((i, j))
                else:
                    ptn.append((i, j))
    # 有伴电压源，双方电流添加±UG，电导为G不变
    for elem in ptn:
        bp[elem[0]][0] += ap[elem[0]][elem[1]] * cp[elem[0]][elem[1]]
        bp[elem[1]][0] -= ap[elem[0]][elem[1]] * cp[elem[0]][elem[1]]

    # 自导行相加，互导取负
    for i in range(0, n):
        for j in range(0, n):
            ap[i][j] *= -1
        ap[i][i] = sum(ap[i])
        ap[i][i] *= -1

    # 独立电压源，系数矩阵加一列，电压源两端结点对应的行的此列为±1，此列其余为0；
    # 增加一行，此行2个对应结点电压相减为电源电压；电导无穷大，列式子的时候用0代替。
    # 结果前n个不变，为n个结点电压，附加一个电压源电流
    for elem in nptn:
        for i in range(0, n):
            if i == elem[0]:
                ap[i].append(-1 * numpy.sign(cp[elem[0]][elem[1]]))
            elif i == elem[1]:
                ap[i].append(numpy.sign(cp[elem[0]][elem[1]]))
            else:
                ap[i].append(0)
        ap.append([0] * (n + 1))
        ap[n][elem[0]] = 1
        ap[n][elem[1]] = -1
        ap[n][n] = cp[elem[0]][elem[1]]

    # 转化为ndarray对象，计算结点电压
    a = numpy.array(ap, dtype=float)  # 将多维列表转化为numpy库下的矩阵
    # if sheet.cell(rf, cf).value in ['r', 'R']:  # 取倒数，将电阻转化为电导
    # a = numpy.reciprocal(a)
    print('A=', a)

    b = numpy.array(bp, dtype=float)
    print('B=', b)

    x = numpy.linalg.solve(a, b)  # 求解线性方程组
    print('x=', x)

    return x


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 90, 351, 461))
        self.textBrowser.setObjectName("textBrowser")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(1, 9, 791, 31))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.filaddlabel = QtWidgets.QLabel(self.splitter_2)
        self.filaddlabel.setMaximumSize(QtCore.QSize(145, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.filaddlabel.setFont(font)
        self.filaddlabel.setObjectName("filaddlabel")
        self.lineEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.choosefile = QtWidgets.QPushButton(self.splitter_2)
        self.choosefile.setMaximumSize(QtCore.QSize(200, 16777215))
        self.choosefile.setObjectName("choosefile")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 90, 391, 461))
        self.label.setStyleSheet("image: url(233.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.U = QtWidgets.QLabel(self.centralwidget)
        self.U.setGeometry(QtCore.QRect(400, 370, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.U.setFont(font)
        self.U.setObjectName("U")
        self.R = QtWidgets.QLabel(self.centralwidget)
        self.R.setGeometry(QtCore.QRect(410, 230, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.R.setFont(font)
        self.R.setObjectName("R")
        self.nodeVol = QtWidgets.QPushButton(self.centralwidget)
        self.nodeVol.setGeometry(QtCore.QRect(0, 50, 351, 31))
        self.nodeVol.setObjectName("nodeVol")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(370, 50, 421, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.jiedian1 = QtWidgets.QLineEdit(self.splitter)
        self.jiedian1.setObjectName("jiedian1")
        self.jiedian2 = QtWidgets.QLineEdit(self.splitter)
        self.jiedian2.setObjectName("jiedian2")
        self.daiweining = QtWidgets.QPushButton(self.splitter)
        self.daiweining.setObjectName("daiweining")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionhelp = QtWidgets.QAction(MainWindow)
        self.actionhelp.setObjectName("actionhelp")
        self.menu.addAction(self.actionhelp)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "电路1 李程浩"))
        self.filaddlabel.setText(_translate("MainWindow", "Excel文件地址："))
        self.choosefile.setText(_translate("MainWindow", "选择Excel文件"))
        self.U.setText(_translate("MainWindow",
                                  "<html><head/><body><p align=\"right\">U<span style=\" vertical-align:sub;\">oc</span></p></body></html>"))
        self.R.setText(_translate("MainWindow",
                                  "<html><head/><body><p align=\"right\">R<span style=\" vertical-align:sub;\">eq</span></p></body></html>"))
        self.nodeVol.setText(_translate("MainWindow", "节点电压法"))
        self.label_2.setText(_translate("MainWindow", "端口结点"))
        self.daiweining.setText(_translate("MainWindow", "戴维宁等效电路"))
        self.menu.setTitle(_translate("MainWindow", "帮助"))
        self.actionhelp.setText(_translate("MainWindow", "help"))

        self.choosefile.clicked.connect(self.getpath)
        self.nodeVol.clicked.connect(self.nvm)
        self.daiweining.clicked.connect(self.dwn)

    def getpath(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx *.xls)')
        print(openfile_name)
        self.write_path(openfile_name[0])

    def write_path(self, fileadd):
        self.lineEdit.setText(fileadd)
        # print(self.lineEdit.text())

    def open_excel(self):
        # 打开Excel文件
        add = self.lineEdit.text()
        # 从excel中获取数据
        wb = xlrd.open_workbook(add)  # 打开excel文件
        sheet = wb.sheet_by_index(0)  # 选取第一页
        return sheet

    def get_mat(self):
        # 从Excel中读取各个矩阵，返回结点个数n，电导矩阵ap，电流源列向量bp，电压源矩阵cp，无穷大电导下标列表wqd

        # 打开Excel文件
        sheet = self.open_excel()
        row = sheet.nrows  # 保存最大行数、列数，为之后提供范围
        col = sheet.ncols

        # 寻找表头
        bp = False  # 用于break退出双重循环
        for i in range(row):  # 用r,R,g,G表头寻找表格
            for k in range(col):
                if sheet.cell(i, k).value in ['g', 'G']:
                    print('表头在(', i, ',', k, ')')
                    rf = i
                    cf = k
                    bp = True
                    break
            if bp:  # 退出第二重循环
                break
        i = rf + 1  # 单元格位置坐标，从表头右下角一个单元格开始
        k = cf + 1
        while sheet.cell_type(rf, k) == 2:
            k += 1
        n = k - cf - 1  # 结点数目
        k = cf + 1

        # 读取电导
        wqd = []  # 存储无穷大电导的下标
        ap = []  # 用于存储电导矩阵
        tem = []  # 用于存储每行电导
        while sheet.cell_type(i, k) == 2 or sheet.cell_type(i, k) == 1:
            while sheet.cell_type(i, k) == 2 or sheet.cell_type(i, k) == 1:
                v = sheet.cell(i, k).value  # 取特定单元格的值
                if v == '∞':
                    tem.append(0)
                    wqd.append((i - rf - 1, k - cf - 1))
                else:
                    tem.append(v)  # 将新单元格的值添加到tem的末尾
                k += 1
                if k >= col:  # 假如此表格就在页面的右下角，则需要避免使用value读取超过范围的单元格，所以用if退出循环
                    break
            ap.append(tem)  # 将本行数据tem添加到a中
            tem = []  # tem置空，用于下一行
            i += 1
            if i >= row:
                break
            k = cf + 1

        # 从上到下读取电流源的值，并存储在列矩阵b中
        bp = []
        for sb in range(rf + 1, rf + 1 + n):
            if sheet.cell_type(sb, cf + 2 + n) == 2:
                bp.append([sheet.cell(sb, cf + 2 + n).value])
            else:
                bp.append([0])

        # 电压源
        cp = []
        for i in range(rf + 1, rf + 1 + n):
            cp.append(sheet.row_values(i, cf + n + 5, cf + 2 * n + 5))

        # 计算所需矩阵一起返回
        mat = (n, ap, bp, cp, wqd)
        return mat

    def nvm(self):
        # 节点电压法函数，与节点电压法按钮连接
        read = self.get_mat()
        n = read[0]
        ap = read[1]
        bp = read[2]
        cp = read[3]
        wqd = read[4]

        x = calclt(n, ap, bp, cp, wqd)

        # GUI输出结点电压
        self.textBrowser.clear()
        self.textBrowser.append('各节点电压为：\n')
        for ind in range(0, n):
            self.textBrowser.append(str(ind + 1) + '.  ' + str(x[ind][0]))

    def read_node(self):
        n1 = int(self.jiedian1.text())
        n2 = int(self.jiedian2.text())
        return n1, n2

    def dwn(self):
        # 戴维宁等效电路求解
        n1, n2 = self.read_node()

        read = self.get_mat()
        n = read[0]
        ap = read[1]
        bp = read[2]
        cp = read[3]
        wqd = read[4]

        # 计算结点电压差du1
        x = calclt(n, ap, bp, cp, wqd)
        read = self.get_mat()
        n = read[0]
        ap = read[1]
        bp = read[2]
        cp = read[3]
        wqd = read[4]
        x = list(x)
        x.append(0)
        du1 = x[n1 - 1][0] - x[n2 - 1][0]

        # 计算开路电压du
        ap[n1 - 1][n2 - 1] = 0
        ap[n2 - 1][n1 - 1] = 0
        x = calclt(n, ap, bp, cp, wqd)
        read = self.get_mat()
        n = read[0]
        ap = read[1]
        bp = read[2]
        cp = read[3]
        wqd = read[4]
        x = list(x)
        x.append(0)
        du = x[n1 - 1][0] - x[n2 - 1][0]

        # 增添1A电流源以计算等效电阻
        if n1 != 0:
            bp[n1 - 1][0] += 1
        if n2 != 0:
            bp[n2 - 1][0] -= 1
        x = calclt(n, ap, bp, cp, wqd)
        x = list(x)
        x.append(0)
        du2 = x[n1 - 1][0] - x[n2 - 1][0]
        r = abs(du2 - du1)

        # GUI输出计算结果
        self.U.clear()
        self.R.clear()
        self.U.setText(str(du) + 'V')
        self.R.setText(str(r) + 'S')


if __name__ == '__main__':
    import sys
    import numpy
    import xlrd

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
