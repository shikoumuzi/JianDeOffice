from PyQt5.QtCore import QThread, pyqtSignal


class OfficeSearchThread(QThread):
    # 定义信号
    success = pyqtSignal(list)
    error = pyqtSignal()

    def __init__(self, searchfun, col, time, text, dataflag, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.searchfun = searchfun
        self.col = col
        self.text = text
        self.starttime = time
        self.dataflag = dataflag

    def run(self):
        # 发送信号
        searchresult = self.searchfun(col=self.col, text=self.text, dataflag=self.dataflag,
                                      starttime=self.starttime)
        if searchresult != None:
            self.success.emit(searchresult)
        else:
            self.error.emit()
        pass


DATACTRLSIGNALSTAT = {"ADD": 0,
                      "CHANGE": 1,
                      "ERASE": 2,
                      "GIVEBACK": 3,
                      "BORROW": 4}


# 专门控制数据io
class OfficeDataCtrlThread(QThread):
    success = pyqtSignal(list, int, int, str, bool)
    error = pyqtSignal(list, int, int, str, bool)

    def __init__(self, datactrlfun, checkfun, data, flag, dataflag, pos, *args, **kwargs):
        super(OfficeDataCtrlThread, self).__init__(*args, **kwargs)
        self.flag = flag
        self.datactrlfun = datactrlfun
        self.checkfun = checkfun
        self.data = data
        self.pos = pos
        self.dataflag = dataflag
        pass

    # 调用数据处理函数
    def run(self) -> None:
        if self.flag == DATACTRLSIGNALSTAT["ADD"]:
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
            datasubmitlist = [self.data["class"],
                              self.data["name"],
                              self.data["id"],
                              self.data["phone"],
                              self.data["college"],
                              self.data["department"],
                              self.data["goodsorplace"],
                              self.data["starttime"],
                              self.data["endtime"],
                              "否",
                              "否",
                              self.data["remark"]]

            if self.checkfun(data = datasubmitlist, dataflag=self.dataflag) == []:
                self.error.emit([], 0, self.pos, self.dataflag, False)
                return

            self.datactrlfun(datasubmitlist)
            self.success.emit(datasubmitlist, DATACTRLSIGNALSTAT["ADD"], self.pos, self.dataflag, True)
        else:
            print("error")

        pass


class OfficeCryptDataThread(QThread):
    success = pyqtSignal(str, bool)
    error = pyqtSignal(str, bool)

    def __init__(self, checkcryptedfun, username, pwd):
        super(OfficeCryptDataThread, self).__init__()
        self.CheckCryptedFun = checkcryptedfun
        self.username = username
        self.pwd = pwd

    def run(self) -> None:
        if self.CheckCryptedFun(username=self.username, pwd=self.pwd):
            self.success.emit(self.username, True)
        else:
            self.error.emit(None, False)
