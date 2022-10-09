import sys
from PyQt5.QtWidgets\
    import QApplication
from OfficeExcel import OfficeExcel as excel
from OfficeUI import*
from OfficeManager import OfficeManager as manager


title_data = {"A1": "班级",
              "B1": "姓名",
              "C1": "学号",
              "D1": "联系方式",
              "E1": "学院/书院",
              "F1": "组织/部门",
              "G1": "借用物资",
              "H1": "借用日期",
              "I1": "归还日期",
              "J1": "是否已借出",
              "K1": "是否归还",
              "L1": "备注",
              "M1": "编号"}
title_data_list = []
for key in title_data.keys():
    col_title = [title_data[key], 100]
    title_data_list.append(col_title)

# print("查找到的")
# print(goods_excel.data_find("B", "陈伊婷"))

# print("写入得")
# print(goods_excel.data_find("B", "危云菲"))

app = QApplication(sys.argv)

window = manager(table_title=title_data_list)

# window.goods_excel.data_write(data_row)
# window.windows.excel_windows_goods.TableWrite(now_row=0, table_2index=window.goods_excel.data_read())
# window.windows.excel_windows_goods.show()

sys.exit(app.exec_())
