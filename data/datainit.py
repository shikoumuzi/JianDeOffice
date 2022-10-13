import hashlib
import os

file = open("user.txt", "a+")

md5 = hashlib.md5("shikoumuziinjiande".encode("utf-8"))
md5.update("1234567".encode("utf-8"))
pwd = md5.hexdigest()

file.close()

