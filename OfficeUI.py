import sys
import PySide2

from PyQt5.QtCore import Qt, QDate, QEvent
from PyQt5.QtWidgets \
    import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, \
    QMessageBox, QComboBox, QMainWindow, QCalendarWidget, QDateEdit, QSizePolicy, \
    QDateTimeEdit

from PyQt5.QtGui import QImage, QPalette, QPixmap

import datetime
from OfficeThread import *


class ExcelWindows(QWidget):
    def __init__(self,
                 search_success_callback,
                 search_error_callback,
                 searchfun,
                 datactrl_callback,
                 datactrl_success_result,
                 datactrl_error_result,
                 dataflag,
                 table_title: list, height=1227, width=500):
        super().__init__()

        # 声明未定义的变量以及部分继承的变量
        self.txt_search_data = None
        self.cb_search_col = None
        self.searchfun_callback = searchfun
        self.col_litter_combox = None
        self.col_time_combox = None
        self.excel_th = None
        self.success_callback = search_success_callback
        self.error_callback = search_error_callback
        self.data_ctrl_callback = datactrl_callback
        self.datactrl_success_result = datactrl_success_result
        self.datactrl_error_result = datactrl_error_result
        self.data_th = None
        self.dataflag = dataflag
        # 窗口标题
        self.setWindowTitle("JianDe Office")

        # 窗口尺寸
        self.resize(height, width)
        # 窗口位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # #调出空白窗体
        # self.show()
        # 创建垂直方向总体布局
        layout = QVBoxLayout()
        layout.addLayout(self.__HeaderInit())
        layout.addLayout(self.__FormInit(table_title))
        table_layout, table_widget = self.__TableInit(row=0, col=table_title.__len__(), table_title=table_title)
        layout.addLayout(table_layout)
        layout.addLayout(self.__FooterInit())

        # 添加底部弹簧
        # layout.addStretch()

        # 元素的排列方式
        self.setLayout(layout)
        self.table_widget = table_widget

    def __HeaderInit(self):
        # 1、创建顶部菜单布局
        header_layout = QHBoxLayout()
        # 添加按钮部件
        bin_start = QPushButton("开始")
        header_layout.addWidget(bin_start)
        header_layout.addStretch()
        return header_layout

    def __FormInit(self, table_title):
        # 2、创建上面搜索框布局
        form_layout = QHBoxLayout()

        table_datas = []
        for data in table_title:
            table_datas.append(data[0])

        # 创建输入框
        # txt_column = QLineEdit()
        # txt_column.setPlaceholderText("情输入要搜索的列")
        # txt_column.setMaximumWidth(200)
        # form_layout.addWidget(txt_column)
        cb_col = QComboBox(self)
        cb_col.addItems(table_datas)
        form_layout.addWidget(cb_col)

        cb_time = QComboBox(self)
        cb_time.addItems(["一个月内", "半年内", "一年内"])
        form_layout.addWidget(cb_time)

        txt_search = QLineEdit()
        txt_search.setPlaceholderText("请输入搜索的姓名")

        # 设置响应回车事件
        txt_search.returnPressed.connect(self.search_click)
        form_layout.addWidget(txt_search)

        bin_search = QPushButton("搜索")
        # 连接槽函数
        bin_search.clicked.connect(self.search_click)

        form_layout.addWidget(bin_search)

        self.col_time_combox = cb_time
        self.col_letter_combox = cb_col
        self.txt_search_data = txt_search
        return form_layout

    def search_time(self, time):
        date_time = datetime.datetime.now()
        ret = ""
        if time == "一个月内":
            date_time = date_time + datetime.timedelta(days=-30)
            pass
        elif time == "半年内":
            date_time = date_time + datetime.timedelta(days=-180)
            pass
        elif time == "一年内":
            date_time = date_time + datetime.timedelta(days=-365)
            pass
        return date_time

    def search_click(self):
        # 获取输入框中的内容
        text = self.txt_search_data.text()
        coltime = self.col_time_combox.currentText()
        colletter = self.col_letter_combox.currentText()
        self.excel_th = OfficeSearchThread(searchfun=self.searchfun_callback,
                                           col=colletter, time=self.search_time(coltime),
                                           dataflag=self.dataflag, text=text)
        self.excel_th.success.connect(self.success_callback)
        self.excel_th.error.connect(self.error_callback)
        self.excel_th.start()

    def __TableInit(self, row, col, table_title=None):
        # 3、创建中间表格布局
        table_layout = QHBoxLayout()
        table_widget = QTableWidget(row, col)  # 几行几列

        # 设置横向标题文字
        # item = QTableWidgetItem()
        # item.setText("标题")  # 设置文字
        # table_widget.setHorizontalHeaderItem(0, item)
        # table_widget.setColumnWidth(1, 200)

        if table_title is not None:
            for i in range(table_title.__len__()):
                item = QTableWidgetItem()
                item.setText(table_title[i][0])  # 设置文字
                table_widget.setHorizontalHeaderItem(i, item)
                table_widget.setColumnWidth(i, table_title[i][1])

        # current_row_count = table_widget.rowCount()
        # table_2index = [[1, 0], [1, 0]]
        # for row in table_2index:
        #     table_widget.insertRow(current_row_count)
        #     current_row_count += 1

        table_layout.addWidget(table_widget)
        return table_layout, table_widget

    def TableWrite(self, now_row=None, table_2index=None, table_index=None):
        current_row_count = 0
        # print(table_2index)
        if now_row is None:
            current_row_count = self.table_widget.rowCount()
        else:
            current_row_count = now_row
        if table_2index is not None:
            i = 0
            for row in table_2index:
                self.table_widget.insertRow(current_row_count)
                for cell_data in row:
                    if str(cell_data) == "":
                        cell_data = " "
                    cell = QTableWidgetItem(str(cell_data))
                    # 设置单元格不可修改
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table_widget.setItem(current_row_count, i, cell)
                    i += 1
                i = 0
                current_row_count += 1
        elif table_index is not None:
            self.table_widget.insertRow(current_row_count)
            i = 0
            for cell_data in table_index:
                cell = QTableWidgetItem(str(cell_data))
                # 设置单元格不可修改
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(current_row_count, i, cell)
                i += 1
        else:
            print("have no data")

    def __FooterInit(self):
        # 4、创建底部菜单布局
        bottom_layout = QHBoxLayout()
        lable_stat = QLabel("JianDe")
        bottom_layout.addWidget(lable_stat)
        bottom_layout.addStretch()

        bottom_add = QPushButton("增加")
        bottom_add.clicked.connect(self.data_add)
        bottom_change = QPushButton("修改")
        bottom_borrow = QPushButton("借出")

        bottom_giveback = QPushButton("归还")
        bottom_close = QPushButton("关闭")

        bottom_layout.addWidget(bottom_add)
        bottom_layout.addWidget(bottom_change)
        bottom_layout.addWidget(bottom_borrow)
        bottom_layout.addWidget(bottom_giveback)
        bottom_layout.addWidget(bottom_close)

        return bottom_layout

    # 获取数据
    def data_ctrl(self, flag):
        if flag == DATACTRLSIGNALSTAT["ADD"]:
            self.data_ctrl_callback(self.dataflag, DATACTRLSIGNALSTAT["ADD"])
            pass
        elif flag == DATACTRLSIGNALSTAT["CHANGE"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["ERASE"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["GIVEBACK"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["BORROW"]:
            pass

    # {"ADD": 0,
    #  "CHANGE": 1,
    #  "ERASE": 2,
    #  "GIVEBACK": 3,
    #  "BORROW": 4}
    def data_add(self):
        self.data_ctrl(flag=DATACTRLSIGNALSTAT["ADD"])

    def data_erase(self):
        self.data_ctrl(flag=DATACTRLSIGNALSTAT["ERASE"])

    def data_change(self):
        self.data_ctrl(flag=DATACTRLSIGNALSTAT["CHANGE"])

    def data_giveback(self):
        self.data_ctrl(flag=DATACTRLSIGNALSTAT["GIVEBACK"])

    def data_borrow(self):
        self.data_ctrl(flag=DATACTRLSIGNALSTAT["BORROW"])


class ExcelSearchWindows(QWidget):
    def __init__(self, uiparent, windowstitle: str, table_title: list, row, col, pos: int):
        super(ExcelSearchWindows, self).__init__()

        super().__init__()
        self.setWindowTitle(windowstitle)
        self.resize(800, 500)
        self.uiparent = uiparent
        self.pos = pos  # #窗口位置
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().right()
        # qr.moveCenter(cp)

        self.table_widget = None

        layout = QHBoxLayout()
        layout.addLayout(self.TableInit(table_title=table_title, row=row, col=col))

        self.setLayout(layout)

    def TableInit(self, table_title: list, row: int, col: int):
        table_layout = QHBoxLayout()
        table_widget = QTableWidget(row, col)
        # 设置横向标题文字
        if table_title != None:
            for i in range(table_title.__len__()):
                item = QTableWidgetItem()
                item.setText(table_title[i][0])  # 设置文字
                table_widget.setHorizontalHeaderItem(i, item)
                table_widget.setColumnWidth(i, table_title[i][1])

        table_layout.addWidget(table_widget)
        self.table_widget = table_widget
        return table_layout
        pass

    def TableWrite(self, table_2index: list):
        # self.table_widget.clear()
        current_row_count = 0
        i = 0
        for row in table_2index:
            self.table_widget.insertRow(current_row_count)
            for cell_data in row:
                cell = QTableWidgetItem(str(cell_data))
                # 设置单元格不可修改
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table_widget.setItem(current_row_count, i, cell)
                i += 1
            i = 0
            current_row_count += 1

        pass

    def close(self) -> bool:
        self.setParent(None)
        self.deleteLater()
        self.uiparent.excel_search_windows.pop(self.pos)
        return super(ExcelSearchWindows, self).close()


class ExcelDataCtrlWindows(QWidget):
    def __init__(self,
                 datasubmitfun,
                 windowsparnet,
                 uiparent,
                 pos,
                 dataflag="GOODS"):
        super(ExcelDataCtrlWindows, self).__init__()

        self.setWindowTitle("数据操作")

        layout = QVBoxLayout()

        name_lineedit = QLineEdit()
        name_lineedit.setPlaceholderText("请输入姓名")

        class_lineedit = QLineEdit()
        class_lineedit.setPlaceholderText("请输入班级")

        id_lineedit = QLineEdit()
        id_lineedit.setPlaceholderText("请输入学号")

        phone_lineedit = QLineEdit()
        phone_lineedit.setPlaceholderText("请输入联系方式")

        department_lineedit = QLineEdit()
        department_lineedit.setPlaceholderText("请输入组织/部门")

        college_lineedit = QLineEdit()
        college_lineedit.setPlaceholderText("请输入学院/书院")

        remark_lineedit = QLineEdit()
        remark_lineedit.setPlaceholderText("请输入备注")

        self.name = name_lineedit
        self.class_name = class_lineedit
        self.id = id_lineedit
        self.phone = phone_lineedit
        self.college = college_lineedit
        self.remark = remark_lineedit
        self.start_date = None
        self.end_date = None
        self.department = department_lineedit
        self.datasubmitfun = datasubmitfun
        self.goodslineedit = None
        self.placecombox = None
        self.uiparent = uiparent
        self.windowsparnet = windowsparnet
        self.pos = pos
        self.dataflag = dataflag

        layout.addWidget(name_lineedit)
        layout.addWidget(class_lineedit)
        layout.addWidget(id_lineedit)
        layout.addWidget(phone_lineedit)
        layout.addWidget(college_lineedit)
        layout.addWidget(department_lineedit)

        if dataflag == "GOODS":
            self.goodslineedit = self.__GoodsInit()
            layout.addWidget(self.goodslineedit)
            # 缺少查询函数
        else:
            self.placecombox = self.__PlaceInit()
            self.placecomboxdata = None
            self.placecombox.currentIndexChanged[str].connect(self.placecomboxdata)
            layout.addWidget(self.thingslineedit)
            # 缺少处理函数

        self.start_date = self.__GivebackAndBorrowInit(1)
        self.end_date = self.__GivebackAndBorrowInit(0)

        layout.addWidget(self.start_date)
        layout.addWidget(self.end_date)
        layout.addWidget(remark_lineedit)

        bottom_submit = QPushButton("提交")
        bottom_submit.clicked.connect(self.datasubmit)

        layout.addWidget(bottom_submit)
        self.resize(300, 300)
        self.setLayout(layout)

    # 做拦截事件，执行enter提交
    def event(self, event) -> bool:
        if event.type() == QEvent.KeyPress and event.key() in (
                Qt.Key_Enter,
                Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(event)

    def __GoodsInit(self):
        goods_lineedit = QLineEdit()
        goods_lineedit.setPlaceholderText("请输入物资")

        return goods_lineedit

    def __PlaceInit(self):
        place_combox = QComboBox(self)
        place_combox.addItems(["4-103", "6-103"])
        return place_combox

    def __GivebackAndBorrowInit(self, flag: int):
        ret = None
        if flag == 1:
            # giveback_lineedit = QLineEdit()
            # giveback_lineedit.setPlaceholderText("请输入借出时间")
            # ret = giveback_lineedit

            start_date = QDateTimeEdit(QDate.currentDate())
            start_date.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # 设置日期格式
            start_date.setMinimumDate(QDate.currentDate().addDays(-30))  # 设置最小日期
            start_date.setMaximumDate(QDate.currentDate().addDays(30))  # 设置最大日期
            start_date.setCalendarPopup(True)
            ret = start_date
        else:
            # borrow_lineedit = QLineEdit()
            # borrow_lineedit.setPlaceholderText("请输入归还时间")
            # ret = borrow_lineedit

            end_date = QDateTimeEdit(QDate.currentDate())
            end_date.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # 设置日期格式
            end_date.setMinimumDate(QDate.currentDate().addDays(-30))  # 设置最小日期
            end_date.setMaximumDate(QDate.currentDate().addDays(30))  # 设置最大日期
            end_date.setCalendarPopup(True)
            ret = end_date
        return ret

    def placecomboxinit(self, place):
        self.placecomboxdata = place

    def datasubmit(self):
        name = self.name.text()
        class_name = self.class_name.text()
        id = self.id.text()
        phone = self.phone.text()
        college = self.college.text()
        department = self.department.text()
        remark = self.remark.text()
        start_date = self.start_date.text()
        end_date = self.end_date.text()

        data_submit = {"name": name,
                       "class": class_name,
                       "id": id,
                       "phone": phone,
                       "college": college,
                       "goodsorplace": None,
                       "department": department,
                       "remark": remark,
                       "starttime": start_date,
                       "endtime": end_date}

        if self.goodslineedit is not None:
            goods = self.goodslineedit.text()
            data_submit["goodsorplace"] = goods
        elif self.placecombox is not None:
            placedata = self.placecomboxdata
            data_submit["goodsorplace"] = placedata
        pass

        self.datasubmitfun(datasubmitlist=data_submit,
                           flag=DATACTRLSIGNALSTAT["ADD"],
                           dataflag=self.dataflag, pos=self.pos)

    def close(self) -> bool:
        self.setParent(None)
        self.deleteLater()
        self.uiparent.excel_datactrl_windows.pop(self.pos)
        return super(ExcelDataCtrlWindows, self).close()


class SignInWindows(QWidget):
    def __init__(self, cryptedfun):
        super(SignInWindows, self).__init__()
        self.cryptedfun = cryptedfun
        self.setWindowTitle("登录")

        layout = QVBoxLayout()
        self.username_lineedit = QLineEdit()
        self.pwd_lineedit = QLineEdit()
        self.pwd_lineedit.hide()
        submit_button = QPushButton("提交")
        submit_button.clicked.connect(self.SubmitUserMessahe)

        layout.addWidget(self.username_lineedit)
        layout.addWidget(self.pwd_lineedit)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def SubmitUserMessage(self):
        username = self.username_lineedit.text()
        password = self.pwd_lineedit.text()
        self.cryptedfun(username, password)


class MainWindows(QMainWindow):
    def __init__(self, image_path,
                 goods_begin, place_begin,
                 signin_begin, close_end):
        super(MainWindows, self).__init__()

        # 主界面必须内嵌一个中心widget 才能够调用
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle("JianDeOffice")
        # 窗口尺寸
        self.resize(1227, 500)
        # 窗口位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        layout = QHBoxLayout()

        self.image = QImage(image_path)
        self.image_label = self.LogoInit()
        self.image_label.setGeometry(0, 0, 400, 400)
        layout.addWidget(self.image_label)

        button_layout = self.AllButtonInit(goods_begin=goods_begin, place_begin=place_begin,
                                            signin_begin=signin_begin, close_end=close_end)


        self.username_label = QLabel("未登录")
        button_layout.addWidget(self.username_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        self.centralwidget.setLayout(layout)

    def LogoInit(self):
        image_label = QLabel()
        image_label.setBackgroundRole(QPalette.Base)
        image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        image_label.setScaledContents(True)
        image_label.setPixmap(QPixmap.fromImage(self.image))
        return image_label

    def ButtonInit(self, buttonname, connectfun):
        button = QPushButton(buttonname)
        # button.clicked.connect(connectfun)
        return button

    def AllButtonInit(self,
                      goods_begin, place_begin,
                      signin_begin, close_end):
        button_layout = QVBoxLayout()
        button_layout.addStretch()
        office_basework_layout = QHBoxLayout()
        button_goods = self.ButtonInit(buttonname="物资", connectfun=goods_begin)
        button_place = self.ButtonInit(buttonname="场地", connectfun=place_begin)
        button_goods.resize(50, 30)
        button_place.resize(50, 30)
        office_basework_layout.addWidget(button_goods)
        office_basework_layout.addWidget(button_place)

        software_beasework_layout = QHBoxLayout()
        button_sigin = self.ButtonInit(buttonname="登录", connectfun=signin_begin)
        button_close = self.ButtonInit(buttonname="关闭", connectfun=close_end)
        button_sigin.resize(50, 30)
        button_close.resize(50, 30)
        software_beasework_layout.addWidget(button_sigin)
        software_beasework_layout.addWidget(button_close)

        button_layout.addLayout(office_basework_layout)
        button_layout.addLayout(software_beasework_layout)
        return button_layout

    def setSignStatus(self, status):
        self.username_label.setText(status)


class OfficeUI:
    def __init__(self, colnum):
        self.main_windows = None
        self.excel_windows_goods = None
        self.excel_windows_place = None
        self.colnum = colnum

        self.sign_windows = None
        self.excel_search_windows = []
        self.excel_datactrl_windows = []

    def CreateSignInWindows(self, cryptedfun):
        self.sign_windows = SignInWindows(cryptedfun=cryptedfun)
        self.sign_windows.show()

    def CreateMainWinows(self, image_path,
                         goods_begin=None, place_begin=None,
                         signin_begin=None, close_end=None):
        self.main_windows = MainWindows(image_path=image_path,
                                        goods_begin=goods_begin, place_begin=place_begin,
                                        signin_begin=signin_begin, close_end=close_end)
        self.main_windows.show()
        pass

    def CreateExcelWindows(self, excelwindows_arg: dict):
        self.excel_windows_goods \
            = ExcelWindows(searchfun=excelwindows_arg["search"]["searchfun"],
                           search_success_callback=excelwindows_arg["search"]["search_success_callback"],
                           search_error_callback=excelwindows_arg["search"]["search_error_callback"],
                           datactrl_callback=excelwindows_arg["data"]["datactrl_callback"],
                           datactrl_success_result=excelwindows_arg["data"]["datactrl_success_result"],
                           datactrl_error_result=excelwindows_arg["data"]["datactrl_error_result"],
                           dataflag=excelwindows_arg["dataflag"],
                           table_title=excelwindows_arg["table_title"],
                           height=excelwindows_arg["height"],
                           width=excelwindows_arg["width"])

    def CreateExcelSearchWindows(self, windowstitle: str, tabtle_title: list, data_2index: list):
        childwindows = ExcelSearchWindows(uiparent=self,
                                          table_title=tabtle_title,
                                          windowstitle=windowstitle,
                                          pos=self.excel_search_windows.__len__(),
                                          row=data_2index.__len__(),
                                          col=self.colnum)
        self.excel_search_windows.append(childwindows)
        childwindows.TableWrite(table_2index=data_2index)
        childwindows.show()

    def CreateExcelDataCtrlWindows(self, datasubmitfun, dataflag):
        childwindows = ExcelDataCtrlWindows(datasubmitfun=datasubmitfun,
                                            dataflag=dataflag,
                                            windowsparnet=self.excel_windows_goods,
                                            uiparent=self,
                                            pos=self.excel_datactrl_windows.__len__())
        self.excel_datactrl_windows.append(childwindows)
        childwindows.show()

    pass
