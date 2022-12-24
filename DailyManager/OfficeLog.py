import datetime


class OfficeLog:
    def __init__(self):
        self.log_file = open("./data/data.office", "a+")

    def __del__(self):
        self.log_file.close()

    def Log(self, username, data: list):
        self.log_file.write(" ".join(["".join(["[", username, "]"]),
                                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + data + ["\n"]))
