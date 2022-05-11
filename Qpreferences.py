__author__ = "Guixin Chen <Valentinofreeman@163.com>"
__credits__ = ["Jiehuang Liu", "Guixin Chen", "Mingkang Chen",
               "Shuailei Zhao", "HanZhen Fu"]
__license__ = "MIT"
__version__ = "0.0.9"
__maintainer__ = "Guixin Chen"
__email__ = "Valentinofreeman@163.com"
__status__ = "Prototype"


from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QProgressBar,
                             QLabel,
                             QFrame,
                             QHBoxLayout,
                             QVBoxLayout,
                             QTabWidget,
                             QMainWindow,
                             QAction,
                             QStyle,
                             QFileDialog,
                             QStatusBar,
                             QMessageBox,
                             QTextEdit,
                             QDialog
                             )


from PyQt5.QtCore import Qt, QTimer, QSize, QTranslator, QDir, QEvent
from ui_preferences import Ui_Dialog
import Qconfig


class Preferences_win(QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Qconfig.__init__()
        self.setupUi(self)
        self.setWindowTitle('Preferences')
        self.setWindowIcon(QApplication.style().standardIcon(
            QStyle.SP_FileDialogDetailedView))
        self.comboBox.addItems(self.findQmFiles())

        self.pushButtonCD.clicked.connect(self.open_dir)

    def open_dir(self):
        print("Opening image file directory")
        selected_dir = QFileDialog.getExistingDirectory(self, "Open Directory")
        if not selected_dir:
            print("Open image directory failed")
            return None
        else:
            print("selected: "+selected_dir)
            Qconfig.global_resource_directory = selected_dir
            print("Current image directory is: " +
                  Qconfig.global_resource_directory)
            self.append_log("Current image directory is: " +
                            Qconfig.global_resource_directory)

    def findQmFiles(self):
        trans_dir = QDir('translations')
        filename = trans_dir.entryList(['*.qm'], QDir.Files, QDir.Name)
        return [trans_dir.filePath(fn) for fn in filename]
