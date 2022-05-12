# pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package


__author__ = "Jiehuang Liu, Guixin Chen <Valentinofreeman@163.com>"
__credits__ = ["Jiehuang Liu", "Guixin Chen", "Mingkang Chen",
               "Shuailei Zhao", "HanZhen Fu"]
__license__ = "MIT"
__version__ = "0.0.9"
__maintainer__ = "Jiehuang Liu, Guixin Chen"
__email__ = "Valentinofreeman@163.com"
__status__ = "Prototype"

from email import utils
from Carplate import *
from cut_plate import ReadPlate
import Qconfig
import Utils
import sys
import time
import logging
import Qlogging
import Qpreferences
import VideoCapture
from PyQt5.QtGui import QIcon, QPalette, QImage, QPixmap
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
                             QTextEdit
                             )

from PyQt5.QtCore import Qt, QTimer, QSize, QTranslator, QDir, QEvent


def img_cv_to_QImage(img):
    """
    convert cv2 image to QImage
    """
    height, width = img.shape[0], img.shape[1]
    qImg = QImage(img.data, width, height,
                  3 * width, QImage.Format_RGB888).rgbSwapped()
    return QPixmap(qImg)


class result_windows(QMainWindow):
    """
    展示最终的图片和文本的窗口
    参数： cv2图片,字符串
    """

    def __init__(self, img, plate_text):
        super().__init__()
        self.setWindowTitle("Result")

        main_wid = QWidget()

        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setText(plate_text)

        self.label = QLabel(QApplication.translate(
            "result_windows", "Final Result"))
        self.label.setScaledContents(True)
        self.label.setMinimumSize(QSize(40, 30))
        self.label.setMaximumSize(QSize(800, 600))
        converted = img_cv_to_QImage(img)
        self.label.setPixmap(converted)

        btn_copy = QPushButton(QApplication.translate(
            "result_windows", "Copy Car Plate"))
        btn_copy.clicked.connect(self.copy_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.resultTextEdit)
        layout.addWidget(btn_copy)
        main_wid.setLayout(layout)
        self.setCentralWidget(main_wid)

    def copy_text(self):
        text = self.resultTextEdit.toPlainText()
        # self.label.setText(text)
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('The Car++')
        self.setFixedSize(16*60, 9*60)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        # every global_progress_bar_interval ms
        self.timer.start(Qconfig.global_progress_bar_interval)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        self.frame.setObjectName('Frame')
        layout.addWidget(self.frame)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, 0)  # x, y
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>初始化中</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 45, 50)
        self.progressBar.move(100, self.height() - 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Loading</strong>')

        # when progressbar ends
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(0.3)

            self.myApp = MainWindow()
            self.myApp.show()

        self.counter += Qconfig.global_progress_bar_step


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # icon
        self.setWindowIcon(QIcon('Resources\\favicon.ico'))

        # set window specific properties
        self.setWindowTitle("Car++")
        self.window_width, self.window_height = 16*64, 9*64
        self.setMinimumSize(self.window_width, self.window_height)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(True)

        # add tabs
        self.cam_tab = QWidget()
        self.img_tab = QWidget()
        self.log_tab = QWidget()

        # tab name
        self.cam_tab_name = QApplication.translate("MainWindow", "Camera tab")
        self.img_tab_name = QApplication.translate("MainWindow", "Image tab")
        self.log_tab_name = QApplication.translate("MainWindow", "Log tab")

        self.cam_tab.setAutoFillBackground(True)
        self.img_tab.setAutoFillBackground(True)
        self.log_tab.setAutoFillBackground(True)

        self.tabs.addTab(self.img_tab, self.img_tab_name)
        self.tabs.addTab(self.cam_tab, self.cam_tab_name)
        self.tabs.addTab(self.log_tab, self.log_tab_name)

        # add widgets to cam_tab
        self.labelCamTabTitle = QLabel(self.cam_tab)
        self.labelCamTabTitle.setObjectName('LabelCamTabTitle')
        # self.labelCamTabTitle.setText('<strong>Car++</strong>')
        self.labelCamTabTitle.setMinimumSize(QSize(16*10, 9*10))
        self.labelCamTabTitle.setAlignment(Qt.AlignCenter)

        self.btnOpenCamera = QPushButton(
            QApplication.translate("MainWindow", "Open Camera"))
        self.btnOpenCamera.setObjectName("BtnOpenCamera")
        self.btnOpenCamera.setMinimumSize(QSize(16*5, 9*5))
        self.btnOpenCamera.clicked.connect(self.open_camera)

        # cam tab layout
        self.tab_cam_layout = QVBoxLayout()
        self.tab_cam_layout.addWidget(self.labelCamTabTitle)
        self.tab_cam_layout.addWidget(self.btnOpenCamera)

        self.cam_tab.setLayout(self.tab_cam_layout)

        # add widgets to img_tab
        self.btnDetectImg = QPushButton(
            QApplication.translate("MainWindow", "Detect Image"))
        self.btnDetectImg.setObjectName("BtnDetectImg")
        self.btnDetectImg.setMinimumSize(QSize(16*5, 9*5))
        self.btnDetectImg.clicked.connect(self.detect_img)

        self.btnGetResult = QPushButton(
            QApplication.translate("MainWindow", "Result"))
        self.btnGetResult.setObjectName("BtnGetResult")
        self.btnGetResult.setMinimumSize(QSize(16*5, 9*5))
        self.btnGetResult.clicked.connect(self.get_result)
        self.btnGetResult.setEnabled(False)

        # img tab layout
        self.tab_img_layout = QVBoxLayout()
        self.tab_img_layout.addWidget(self.btnDetectImg)
        self.tab_img_layout.addWidget(self.btnGetResult)

        self.img_tab.setLayout(self.tab_img_layout)

        # instantiate Qlogger
        global qlogger
        qlogger = logging.getLogger(__name__)

        # set up Qtext handler
        Qtext_log_handler = Qlogging.QPlainTextEditLogger(self.log_tab)
        format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        Qtext_log_handler.setFormatter(format)
        qlogger.addHandler(Qtext_log_handler)

        self.append_log('Logging started')
        self.append_log("Default image directory is: " +
                        Qconfig.global_resource_directory)
        self.append_log("Default image path is " + Qconfig.global_image_path)

        # find out all the available translations
        qmFiles = self.findQmFiles()
        self.append_log("qmFiles found: " + str(qmFiles))

        # log tab layout
        self.tab_log_layout = QVBoxLayout()
        self.tab_log_layout.addWidget(Qtext_log_handler.widget)

        self.log_tab.setLayout(self.tab_log_layout)

        # menu
        menu = self.menuBar()

        # file menu acciones n.b. ampersand is shortcut
        open_dir_icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        self.acc_open_dir = QAction(open_dir_icon, QApplication.translate(
            "MainWindow", "Open &Folder"), self)
        self.acc_open_dir.setStatusTip(QApplication.translate(
            "MainWindow", "Open a folder to images"))
        self.acc_open_dir.triggered.connect(self.open_dir)

        #open_img_icon = self.style().standardIcon(QStyle.SP_FileIcon)
        open_img_icon = QIcon('Resources\\open_img.png')
        self.acc_open_img = QAction(
            open_img_icon, QApplication.translate("MainWindow", "Open &Image"), self)
        self.acc_open_img.triggered.connect(self.open_img)

        self.acc_exit = QAction(QApplication.translate(
            "MainWindow", "E&xit"), self)
        self.acc_exit.triggered.connect(self.close)

        # file menu
        self.file_menu = menu.addMenu(
            QApplication.translate("MainWindow", "&File"))
        self.file_menu.addAction(self.acc_open_dir)
        self.file_menu.addAction(self.acc_open_img)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.acc_exit)

        # option menu acciones
        self.acc_set_preference = QAction(
            QApplication.translate("MainWindow", "&Preferences"), self)
        self.acc_set_preference.triggered.connect(self.set_preference)

        # option menu
        self.option_menu = menu.addMenu(
            QApplication.translate("MainWindow", "&Options"))
        self.option_menu.addAction(self.acc_set_preference)
        self.option_menu.addSeparator()

        # language submenu
        self.option_language_menu = self.option_menu.addMenu(
            QApplication.translate("MainWindow", "&Language"))
        self.option_language_menu.addAction("&English", self.set_language_en)
        self.option_language_menu.addAction("简体中文[&c]", self.set_language_cn)
        self.option_language_menu.addAction("E&spañol", self.set_language_es)

        # help menu acciones
        self.acc_website = QAction(QApplication.translate(
            "MainWindow", "&Website"), self)
        self.acc_website.triggered.connect(self.open_website)

        self.acc_online_help = QAction(QApplication.translate(
            "MainWindow", "&Online Help"), self)
        self.acc_online_help.triggered.connect(self.open_online_help)

        self.acc_help_md = QAction(
            QApplication.translate("MainWindow", "Show Help (&Markdown)"), self)
        self.acc_help_md.triggered.connect(self.open_help_markdown)

        self.acc_help_html = QAction(QApplication.translate(
            "MainWindow", "Show Help (&HTML)"), self)
        self.acc_help_html.triggered.connect(self.open_help_html)

        self.acc_about = QAction(QApplication.translate(
            "MainWindow", "&About"), self)
        self.acc_about.triggered.connect(self.about)

        # help menu
        self.help_menu = menu.addMenu(
            QApplication.translate("MainWindow", "&Help"))
        self.help_menu.addAction(self.acc_website)
        self.help_menu.addAction(self.acc_online_help)
        self.help_menu.addAction(self.acc_help_md)
        self.help_menu.addAction(self.acc_help_html)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.acc_about)

        # status bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage(QApplication.translate("MainWindow", "Ready"))

        # update translation
        self.retranslateUi()

        # set up main window
        # You can't set a QLayout directly on the QMainWindow
        main_wid = QWidget()
        self.setCentralWidget(main_wid)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        main_wid.setLayout(layout)

    def append_log(self, text):
        qlogger.debug(text)

    def detect_img(self):
        self.append_log("detect_img: current image path: " +
                        Qconfig.global_image_path)
        print("detect_img: current image path: " + Qconfig.global_image_path)
        self.btnGetResult.setEnabled(True)
        selected = carplate(Qconfig.global_image_path)
        #cv2.imshow("selected Rectangle", selected)
        self.result = result_windows(
            selected, QApplication.translate("MainWindow", "Selected Area demonstration"))
        self.result.show()

    def get_result(self):
        self.append_log("call get_result")
        print("call get_result")
        ReadPlate("Resources/Scan/NoPlate_1.jpg")
        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(translate_plate, ())
        # since ReadPlate return Broken image, we load image directly
        img_plate = cv2.imread("Resources/Scan/NoPlate_1.jpg")
        self.result = result_windows(
            img_plate, QApplication.translate("MainWindow", "Calculating"))
        self.result.show()
        QApplication.processEvents()
        self.result.resultTextEdit.setText(async_result.get(timeout=25))

    def open_camera(self):
        self.append_log("Opening camera ...")
        print("Opening camera")
        VideoCapture.capture()

    # open image file and update config.global_image_path

    def open_img(self):
        print("Open image")
        self.append_log("Open image")
        selected_img_name, file_type = QFileDialog.getOpenFileName(
            self, "Open Image", directory=Qconfig.global_resource_directory, filter='Image Files (*.png *.jpg *.jpeg *.bmp *.webp)')
        if selected_img_name == '':
            # open image file failed
            print("Open image failed")
            self.append_log("Open image failed")
            return None
        else:
            print("selected: "+selected_img_name)
            self.append_log("selected: "+selected_img_name)
            Qconfig.global_image_path = selected_img_name
            print("Current image path is: " + Qconfig.global_image_path)
            self.append_log("Current image path is: " +
                            Qconfig.global_image_path)

    # open image file directory
    def open_dir(self):
        print("Opening image file directory")
        self.append_log("Open image file directory")
        selected_dir = QFileDialog.getExistingDirectory(
            self, "Open Directory", directory=Qconfig.global_resource_directory)
        if not selected_dir:
            print("Open image directory failed")
            self.append_log("Open image directory failed")
            return None
        else:
            print("selected: "+selected_dir)
            self.append_log("selected: "+selected_dir)
            Qconfig.global_resource_directory = selected_dir
            print("Current image directory is: " +
                  Qconfig.global_resource_directory)
            self.append_log("Current image directory is: " +
                            Qconfig.global_resource_directory)

    def set_preference(self):
        print("set_preference")
        self.append_log("set_preference")
        self.preference = Qpreferences.Preferences_win()
        self.preference.show()

    def set_language_en(self):
        print("Set language to English")
        self.append_log("Set language to English")
        Qconfig.global_language = 'en'
        self.change_lang("translations/en.qm")

    def set_language_cn(self):
        print("Set language to Chinese")
        self.append_log("Set language to Chinese")
        Qconfig.global_language = 'zh'
        self.change_lang("translations/zh.qm")

    def set_language_es(self):
        print("Set language to Spanish")
        self.append_log("Set language to Spanish")
        Qconfig.global_language = 'es'
        self.change_lang("translations/es.qm")

    def open_help_markdown(self):
        print("Opening help markdown")
        self.append_log("Opening help markdown")
        Utils.openfile_sys("./Resources/help.md")

    def open_help_html(self):
        print("Opening help html")
        self.append_log("Opening help html")
        Utils.openfile_sys("./Resources/help.html")

    def about(self):
        self.setAutoFillBackground(True)
        text = "Car++ is a car plate recognition software."
        text = "<center>" \
            "<h1>Car++</h1>" \
            "&#8291;" \
            "<img src=Resources\\about.jpg>" \
            "</center>" \
            "<p>Version 0.0.8<br/>" \
            "Copyleft &copy; Jxau Univ.</p>"
        QMessageBox.about(self, "About Car++",
                          text)

    def open_website(self):
        import webbrowser
        webbrowser.open("https://github.com/Cherleng/AutoPlusPlus")

    def open_online_help(self):
        import webbrowser
        webbrowser.open("http://dynamiclab.xyz/Car++")

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

    def change_lang(self, data):
        if Utils.exists(data):
            g_translator.load(data)
            QApplication.instance().installTranslator(g_translator)
        else:
            print("No such file: " + data)
            self.append_log("No such file: " + data)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        _ts = QApplication.translate
        # tabs
        self.tabs.setTabText(self.tabs.indexOf(
            self.cam_tab), _ts("MainWindow", "Camera tab"))
        self.tabs.setTabText(
            self.tabs.indexOf(self.img_tab), _ts("MainWindow", "Image tab"))
        self.tabs.setTabText(self.tabs.indexOf(
            self.log_tab), _ts("MainWindow", "Log tab"))

        # widgets
        self.btnOpenCamera.setText(_ts("MainWindow", "Open Camera"))
        self.btnOpenCamera.setToolTip(_ts("MainWindow", "Open Camera"))
        self.btnDetectImg.setText(_ts("MainWindow", "Detect Image"))
        self.btnDetectImg.setToolTip(_ts("MainWindow", "Detect Image"))
        self.btnGetResult.setToolTip(
            _ts("MainWindow", "You have to detect image first"))

        # menus

        # file menu
        self.file_menu.setTitle(_ts("MainWindow", "&File"))

        # works, deprecated
        # self.file_menu.actions()[0].setText(_ts("MainWindow", "Open &Folder"))

        self.acc_open_dir.setText(_ts("MainWindow", "Open &Folder"))
        self.acc_open_dir.setStatusTip(
            _ts("MainWindow", "Open a folder to images"))
        self.acc_open_img.setText(_ts("MainWindow", "Open &Image"))
        self.acc_open_img.setStatusTip(_ts("MainWindow", "Open an image"))

        self.acc_exit.setText(_ts("MainWindow", "E&xit"))

        # option menu
        self.option_menu.setTitle(_ts("MainWindow", "&Options"))

        self.acc_set_preference.setText(_ts("MainWindow", "&Preferences"))

        self.option_language_menu.setTitle(_ts("MainWindow", "&Language"))

        # help menu
        self.help_menu.setTitle(_ts("MainWindow", "&Help"))

        self.acc_website.setText(_ts("MainWindow", "&Website"))
        self.acc_online_help.setText(_ts("MainWindow", "&Online Help"))
        self.acc_help_md.setText(_ts("MainWindow", "Show Help (&Markdown)"))
        self.acc_help_html.setText(_ts("MainWindow", "Show Help (&HTML)"))

        self.acc_about.setText(_ts("MainWindow", "&About"))

        # status bar
        self.statusBar().showMessage(_ts("MainWindow", "Ready"))


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # load from ini file
    Qconfig.__init__()

    # update path to absolute path
    Qconfig.global_resource_directory = Utils.update_path(
        Qconfig.global_resource_directory)
    Qconfig.global_image_path = Utils.update_path(Qconfig.global_image_path)

    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    # set up translation
    global g_translator
    g_translator = QTranslator()
    if Utils.exists(Qconfig.global_language):
        g_translator.load(Qconfig.global_language)
        app.installTranslator(g_translator)

    # app.setStyle("windowsvista")

    # load style sheet from file
    qss_file = open('style.qss').read()
    app.setStyleSheet(qss_file)

    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
