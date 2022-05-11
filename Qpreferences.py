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
import Utils


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
        self.pushButtonCI.clicked.connect(self.open_img)
        self.comboBox.currentIndexChanged.connect(self.change_lang)

        # load default configuration to the plaintextedit

        self.plainTextEdit.setPlainText(
            "Current Values:\n" + Qconfig.getConfig())

    def change_lang(self):
        """
        change language
        """
        print("Changing language")
        path = self.comboBox.currentText()
        print("changing to: " + path)
        Qconfig.updateConfig("lang", path)

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

    def open_img(self):
        print("Open image")
        selected_img_name, file_type = QFileDialog.getOpenFileName(
            self, "Open Image", filter='Image Files (*.png *.jpg *.jpeg *.bmp *.webp)')
        if selected_img_name == '':
            # open image file failed
            print("Open image failed")
            return None
        else:
            print("selected: "+selected_img_name)
            Qconfig.global_image_path = selected_img_name
            print("Current image path is: " + Qconfig.global_image_path)

    def findQmFiles(self):
        trans_dir = QDir('translations')
        filename = trans_dir.entryList(['*.qm'], QDir.Files, QDir.Name)
        return [trans_dir.filePath(fn) for fn in filename]

    def languageName(self, qmFile):
        """
        convert a qmfile name to languageName 
        """
        translator = QTranslator()
        translator.load(qmFile)

        return translator.translate("MainWindow", "English")

    def qmName(self, tag) -> str:
        """
        convert a tag to qm file name
        """
        path = "translations/" + tag + ".qm"
        if Utils.exists(path):
            return path
