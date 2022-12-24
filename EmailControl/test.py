from Email.EmailOperator import *
from Email.EmailConnection import *
from Email.EmailType import *

connect = EmailConnection("ZhangZi")
connect.setUser("qq", "shikoumuzi@qq.com", "ljqothtkzyuhbdee")
connect.getUser()

emailoperator: EmailOperator = connect.connection()
email = SentEmail()
email.setContent("test")
email.setSender("shikoumuzi@qq.com")
email.setReceiver("gdykdxjdsytwzz@163.com")
email.setSubject("python_test")


print(emailoperator.send(email))
