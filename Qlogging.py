
__author__ = " Guixin Chen <Valentinofreeman@163.com>"
__credits__ = ["Guixin Chen", "Jiehuang Liu",  "Mingkang Chen",
               "Shuailei Zhao", "HanZhen Fu"]
__license__ = "MIT"
__version__ = "0.0.8"
__maintainer__ = "Guixin Chen, Jiehuang Liu "
__email__ = "Valentinofreeman@163.com"
__status__ = "Prototype"


import logging
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import QSize


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        self.setLevel(logging.DEBUG)
        self.widget = QPlainTextEdit(parent)
        self.widget.setObjectName('LogPlainTextEdit')
        self.widget.setMinimumSize(QSize(16*10, 9*10))
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        pass
