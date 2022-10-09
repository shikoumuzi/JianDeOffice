import hashlib
import os

file = open("user.txt", "a+")

md5 = hashlib.md5("shikoumuziinjiande".encode("utf-8"))
md5.update("123456".encode("utf-8"))
pwd = md5.hexdigest()

data = ["李文智", pwd]
file.write("李文智 " + pwd)

file.close()

