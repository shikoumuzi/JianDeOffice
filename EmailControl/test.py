from Email.EmailOperator import *
from Email.EmailConnection import *
from Email.EmailType import *

connect = EmailConnection("ZhangZi")
connect.setUser("qq", "1013740747@qq.com", "cohqdyyjipmqbeed")
connect.getUser()

emailoperator: EmailOperator = connect.connection()
email = SentEmail()
email.setSender("1013740747@qq.com")
email.setReceiver("1013740747@qq.com")
email.setSubject("python_test")
email.setContent("李文智")

print(emailoperator.send(email))
