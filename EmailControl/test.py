from Email.EmailOperator import *
from Email.EmailConnection import *
from Email.EmailType import *



connect = EmailConnection("ZhongZi")
# connect.setUser("qq", "shikoumuzi@qq.com", "ljqothtkzyuhbdee")
connect.getUser()

emailoperator: EmailOperator = connect.connection()
email = SentEmail()
email.setContent("test")
email.setSender("shikoumuzi@qq.com")
email.setReceiver("gdykdxjdsytwzz@163.com")
email.setSubject("python_test")
email.setExcel(r"F:\University\工作\团委\2022\到梦空间成长记录批量导入模板.xlsx")
email.setImage(r"C:\Users\矢口木子\Desktop\photo\【翻唱】夜に駆ける／covered by 神楽七奈.jpg")
print(emailoperator.send(email))

