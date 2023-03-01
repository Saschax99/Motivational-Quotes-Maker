from datetime import datetime
import os


class Logging:
    def __init__(self):
        """define variables and standard"""
        self.path_file = None
        self.date_now = None

        self.encoding = 'utf-8'
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.folder_name = "logging"
        self.folder_start_name = None
        self.loglevel = 1

        self.__create_log_folder()

    def __create_log_folder(self):
        """create log folder if not exists"""
        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)

    def debug(self, string):
        """writing debug message into file"""
        if self.loglevel <= 0:
            self.__writing("[DBG]", string)

    def info(self, string):
        """writing info message into file"""
        if self.loglevel <= 1:
            self.__writing("[INF]", string)

    def warning(self, string):
        """writing warning message into file"""
        if self.loglevel <= 2:
            self.__writing("[WRN]", string)

    def error(self, string):
        """writing error message into file"""
        if self.loglevel <= 3:
            self.__writing("[ERR]", string)

    def configure(self,
                  path=None,
                  folder_name=None,
                  file_start_name=None,
                  encoding=None,
                  loglevel=None):
        """set configurations for logging path for logging, folder_name, file_start_name, encoding and log_level:0-3
        -> 0=All logs, 1=Info and above, 2=Warning and above, 3=Errors """
        if path is not None:
            self.path = path
        if folder_name is not None:
            self.folder_name = folder_name
        if file_start_name is not None:
            self.folder_start_name = file_start_name
        if encoding is not None:
            self.encoding = encoding
        if loglevel is not None:
            self.loglevel = loglevel

    def __update_file_name(self):
        """updating file name with current date in "%Y-%m-%d" format"""
        if self.date_now != datetime.today().strftime("%Y-%m-%d"):
            self.date_now = datetime.today().strftime("%Y-%m-%d")
            self.path_file = os.path.join(self.path, self.folder_name,
                                          self.folder_start_name + "_" + self.date_now + ".log")

    def __writing(self, alarm_type, string):
        """writing into log file """
        self.__update_file_name()
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f'{self.path_file}', 'a', newline='', encoding=self.encoding) as f:
            f.write(datetime_now + " " + alarm_type + ": " + string + "\n")


logging = Logging()  # assigning logging instance so only activating it once
