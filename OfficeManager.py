from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from OfficeExcel import OfficeExcel as excel
from OfficeUI import OfficeUI
from OfficeThread import *
import hashlib

title_data_goods = \
    {"A1": "班级", "B1": "姓名", "C1": "学号",
     "D1": "联系方式", "E1": "学院/书院", "F1": "组织/部门",
     "G1": "借用物资", "H1": "借用日期", "I1": "归还日期",
     "J1": "是否已借出", "K1": "是否归还", "L1": "备注", "M1": "编码"}

title_data_place = \
    {"A1": "班级", "B1": "姓名", "C1": "学号",
     "D1": "联系方式", "E1": "学院/书院", "F1": "组织/部门",
     "G1": "借用物资", "H1": "使用开始时间", "I1": "使用截止时间",
     "J1": "是否已借出", "K1": "是否归还", "L1": "备注", "M1": "编码"}


class OfficeManager:
    def __init__(self, table_title: list):
        self.datactrl = DataCtrl(self)
        self.searchexsit = SearchExsit(self)
        self.mainwindowsevent = MainWindowsEvent(self, "./data/user.txt")

        self.excelwindows_goods = {"search":\
                                       {"searchfun": self.searchexsit.searchexsit,
                                        "search_success_callback": self.searchexsit.search_success_callback,
                                        "search_error_callback": self.searchexsit.search_error_callback},
                                   "data":\
                                       {"datactrl_callback": self.datactrl.windows_data_ctrl,
                                        "data-ctrl_success_result": self.datactrl.windows_data_ctrl_result,
                                        "datactrl_error_result": self.datactrl.windows_data_ctrl_result},
                                   "dataflag": "GOODS",
                                   "table_title": table_title,
                                   "height": 1228,
                                   "width": 500}
        self.excelwindows_place = {"search":\
                                       {"searchfun": self.searchexsit.searchexsit,
                                        "search_success_callback": self.searchexsit.search_success_callback,
                                        "search_error_callback": self.searchexsit.search_error_callback},
                                   "data": \
                                       {"datactrl_callback": self.datactrl.windows_data_ctrl,
                                        "data-ctrl_success_result": self.datactrl.windows_data_ctrl_result,
                                        "datactrl_error_result": self.datactrl.windows_data_ctrl_result},
                                   "dataflag": "PLACE",
                                   "table_title": table_title,
                                   "height": 1228,
                                   "width": 500}

        # self.setCallBack(success=self.search_success_callback, error=self.search_error_callback)
        self.windows = OfficeUI(table_title.__len__(), mainwindwosevent=self.mainwindowsevent)

        # self.windows.CreateExcelWindows(excelwindows_arg=self.excelwindows_goods)
        self.windows.CreateMainWinows(image_path="微信图片_20221008222518.jpg")
        # self.windows.CreateFunctionWindows()

        self.goods_excel = excel(title_data=title_data_goods, filepath=".\\data\\OfficeGoods.xlsx")
        self.place_excel = excel(title_data=title_data_goods, filepath=".\\data\\OfficePlace.xlsx")
        self.goods_stat = excel(filepath=".\\data\\OfficeGoodsStatus.xlsx")
        self.goods_num_dict = {}

        for sheet in self.goods_stat.get_allsheel():
            self.goods_stat.sheet_choose(sheet)
            goods_for_sheet = self.goods_stat.data_read()
            for goods in goods_for_sheet:
                if goods.__len__() < 4:
                    for i in range(goods.__len__(), 4):
                        goods.append(None)
                self.goods_num_dict[goods[0]] = [goods[1], goods[2], goods[3]]

        # print(self.goods_num_dict)
        self.datasubmit = {}
        self.table_title = table_title


class MainWindowsEvent:
    def __init__(self, parent: OfficeManager, usermessage_path: str):
        self.parent = parent
        self.cryptuserdata = CryptData(usermessage_path)
        self.compare_th = None
        self.goods_running = False
        self.place_running = False

    def ComparePwd(self, username, pwd):
        self.compare_th = OfficeCryptDataThread(checkcryptedfun=self.cryptuserdata.isTrue,
                                                username=username, pwd=pwd)
        self.compare_th.success.connect(self.ComparePwdResult)
        self.compare_th.error.connect(self.ComparePwdResult)
        self.compare_th.start()

    def ComparePwdResult(self, username: str, result: bool):
        if result is True:
            self.parent.windows.main_windows.setSignStatus(str)
            self.parent.windows.sign_windows.close()
        else:
            QMessageBox.warning(self.parent.windows.main_windows, "登录失败", "请重新登录")
            self.parent.windows.sign_windows.pwd_lineedit.clear()

    def CallExcelGoodsWindows(self):
        if not self.goods_running:
            self.parent.windows.CreateExcelWindows(self.parent.excelwindows_goods)
            self.parent.windows.\
                excel_windows_goods.TableWrite(now_row=0, table_2index=self.parent.goods_excel.data_read())

    def CallExcelPlaceWindwos(self):
        if not self.place_running:
            self.parent.windows.CreateExcelWindows(self.parent.excelwindows_place)
            self.parent.windows.\
                excel_windows_place.TableWrite(now_row=0, table_2index=self.parent.place_excel.data_read())

    def CallExcelGoodsPlaceStatusWindows(self):
        pass

    def CloseSystem(self):
        del self.parent.windows


class CryptData:
    def __init__(self, usermessage_path: str):
        self.md5 = hashlib.md5("shikoumuziinjiande".encode("utf-8"))
        file = open(usermessage_path)
        usersmeassges = file.readlines()
        self.users = {}
        for usermeassge in usersmeassges:
            user_temp = usermeassge.split(" ")
            self.users[user_temp[0]] = user_temp[1][:-1]
        # print(usersmeassges)
        # print(self.users)
        file.close()

    def __getResult(self, string: str):
        self.md5.update(string.encode("utf-8"))
        return self.md5.hexdigest()

    def isTrue(self, username, pwd):
        try:
            ret = (self.users[username] == self.__getResult(pwd))
            # print(username, self.__getResult(pwd))
            return ret
        except:
            # print(username, self.__getResult(pwd))
            return False


class SearchExsit:
    def __init__(self, parent: OfficeManager):
        self.parent = parent

    # 数据查询模块
    def searchexsit(self, col, text, starttime, dataflag="GOODS", endtime=None):
        print(col, text)
        i = 0
        for x in self.parent.table_title:
            if col == x[0]:
                break
            i += 1
        col_letter = chr(ord('A') + i)
        # print(col_letter)
        search_result = None
        if dataflag == "GOODS":
            search_result = self.parent.goods_excel. \
                data_find_bydatetime(column_letter=col_letter, data=text,
                                     start=starttime, end=endtime)
        else:
            search_result = self.parent.place_excel. \
                data_find_bydatetime(column_letter=col_letter, data=text,
                                     start=starttime, end=endtime)
        if search_result is not None:
            return search_result
        else:
            return []

    def search_success_callback(self, data_2index: list):
        # 更新窗口显示信息
        # QMessageBox.information(self.windows.excel_windows, "查询成功", string)
        # print(data_2index)
        self.parent.windows.CreateExcelSearchWindows(windowstitle="查找结果",
                                                     tabtle_title=self.parent.table_title,
                                                     data_2index=data_2index)

    def search_error_callback(self):
        QMessageBox.warning(self.parent.windows.excel_windows_goods, "查询失败", "查无此纪录")


class DataCtrl:
    def __init__(self, parent: OfficeManager):
        self.parent = parent

    # 数据处理 获取数据 传入绑定事件
    def windows_data_ctrl(self, dataflag: str, flag: int):
        if flag == DATACTRLSIGNALSTAT["ADD"]:
            self.parent.windows.CreateExcelDataCtrlWindows(datasubmitfun=self.windows_data_add_submit,
                                                           dataflag=dataflag)
            pass
        elif flag == DATACTRLSIGNALSTAT["CHANGE"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["ERASE"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["GIVEBACK"]:
            pass
        elif flag == DATACTRLSIGNALSTAT["BORROW"]:
            pass

        pass

    # 得到数据结果, 线程结果的出口
    def windows_data_ctrl_result(self, data_result: list, flag: int, pos: int, issuccess=True):
        print(data_result)
        if issuccess:
            if flag == DATACTRLSIGNALSTAT["ADD"]:
                QMessageBox.information(self.parent.windows.excel_windows_goods, "提交结果", "提交成功")
                self.parent.windows.excel_windows_goods.TableWrite(table_index=data_result)
                pass
            elif flag == DATACTRLSIGNALSTAT["CHANGE"]:
                pass
            elif flag == DATACTRLSIGNALSTAT["ERASE"]:
                pass
            elif flag == DATACTRLSIGNALSTAT["ERASE"]:
                pass
            elif flag == DATACTRLSIGNALSTAT["GIVEBACK"]:
                pass
            elif flag == DATACTRLSIGNALSTAT["BORROW"]:
                pass
        else:
            pass
        print(pos)
        self.parent.windows.excel_datactrl_windows[pos].close()

    # add函数的记录检查
    def windows_data_add_check(self, datasubmitlist: dict):

        # data_submit = {"name": name,
        #                "class": class_name,
        #                "id": id,
        #                "phone": phone,
        #                "college": college,
        #                "goodsorplace": None,
        #                "department": department,
        #                "remark": remark,
        #                "starttime": start_date,
        #                "endtime": end_date}
        start_time = datasubmitlist["starttime"]
        end_time = datasubmitlist["endtime"]
        self.parent.searchexsit.searchexsit(col="借用时间", text=datasubmitlist[start_time],)

        pass

    # add操作的函数入口
    def windows_data_add_submit(self, datasubmitlist: dict, dataflag, flag, pos: int):
        print(datasubmitlist)
        self.datasubmit = datasubmitlist
        if dataflag == "GOODS":
            self.data_th = \
                OfficeDataCtrlThread(datactrlfun=self.parent.goods_excel.data_write,
                                     data=self.datasubmit, checkfun=self.windows_data_add_check,
                                     flag=flag, pos=pos)
        elif dataflag == "PLACE":
            self.data_th = \
                OfficeDataCtrlThread(datactrlfun=self.parent.place_excel.data_write,
                                     data=self.datasubmit, checkfun=self.windows_data_add_check,
                                     flag=flag, pos=pos)

        self.data_th.success.connect(self.windows_data_ctrl_result)
        self.data_th.error.connect(self.windows_data_ctrl_result)
        self.data_th.start()

    def windows_data_erase(self):
        pass

    def windows_data_change(self):
        pass

    def windows_data_giveback(self):
        pass

    def windows_data_borrow(self):
        pass
