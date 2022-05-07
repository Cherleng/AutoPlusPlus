# pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package


__author__ = "Jiehuang Liu, Guixin Chen <Valentinofreeman@163.com>"
__credits__ = ["Jiehuang Liu", "Guixin Chen", "Mingkang Chen",
               "Shuailei Zhao", "HanZhen Fu"]
__license__ = "MIT"
__version__ = "0.0.7"
__maintainer__ = "Jiehuang Liu, Guixin Chen"
__email__ = "Valentinofreeman@163.com"
__status__ = "Prototype"


from Carplate import *
import Config
import Utils
import sys
import time
import logging
import Qlogging
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QProgressBar,
                             QLabel,
                             QFrame,
                             QHBoxLayout,
                             QPlainTextEdit,
                             QVBoxLayout,
                             QTabWidget,
                             QMainWindow,
                             QAction,
                             QStyle,
                             QFileDialog,
                             QStatusBar,
                             QMessageBox
                             )

from PyQt5.QtCore import Qt, QTimer, QSize, QTranslator, QDir


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
        self.timer.start(Config.global_progress_bar_interval)

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

        # self.labelLoading = QLabel(self.frame)
        # self.labelLoading.resize(self.width() - 10, 50)
        # self.labelLoading.move(0, self.progressBar.y() + 70)
        # self.labelLoading.setObjectName('LabelLoading')
        # self.labelLoading.setAlignment(Qt.AlignCenter)
        # self.labelLoading.setText('Loading...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>加载中</strong>')

        # when progressbar ends
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(0.3)

            self.myApp = MainWindow()
            self.myApp.show()

        self.counter += Config.global_progress_bar_step


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.cam_tab.setAutoFillBackground(True)
        self.img_tab.setAutoFillBackground(True)
        self.log_tab.setAutoFillBackground(True)

        self.tabs.addTab(self.cam_tab, self.tr("Camera tab"))
        self.tabs.addTab(self.img_tab, self.tr("Image tab"))
        self.tabs.addTab(self.log_tab, self.tr("Log tab"))

        # add widgets to cam_tab
        self.labelCamTabTitle = QLabel(self.cam_tab)
        self.labelCamTabTitle.setObjectName('LabelCamTabTitle')
        # self.labelCamTabTitle.setText('<strong>Car++</strong>')
        self.labelCamTabTitle.setMinimumSize(QSize(16*10, 9*10))
        self.labelCamTabTitle.setAlignment(Qt.AlignCenter)

        self.btnOpenCamera = QPushButton(self.tr("Open Camera"))
        self.btnOpenCamera.setObjectName("BtnOpenCamera")
        self.btnOpenCamera.setToolTip(self.tr("Open camera"))
        self.btnOpenCamera.setMinimumSize(QSize(16*5, 9*5))
        self.btnOpenCamera.clicked.connect(self.open_camera)

        # cam tab layout
        self.tab_cam_layout = QVBoxLayout()
        self.tab_cam_layout.addWidget(self.labelCamTabTitle)
        self.tab_cam_layout.addWidget(self.btnOpenCamera)

        self.cam_tab.setLayout(self.tab_cam_layout)

        # add widgets to img_tab

        self.btnDetectImg = QPushButton(self.tr("Detect Image"))
        self.btnDetectImg.setObjectName("BtnDetectImg")
        self.btnDetectImg.setToolTip(self.tr("Detect image"))
        self.btnDetectImg.setMinimumSize(QSize(16*5, 9*5))
        self.btnDetectImg.clicked.connect(self.detect_img)

        # img tab layout
        self.tab_img_layout = QVBoxLayout()
        self.tab_img_layout.addWidget(self.btnDetectImg)

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
                        Config.global_resource_directory)
        self.append_log("Default image path is " + Config.global_image_path)

        # log tab layout
        self.tab_log_layout = QVBoxLayout()
        self.tab_log_layout.addWidget(Qtext_log_handler.widget)

        self.log_tab.setLayout(self.tab_log_layout)

        # actions
        # ampersand is shortcut
        open_dir_icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        btn_open_dir = QAction(open_dir_icon, self.tr("Open &Folder"), self)

        open_img_icon = self.style().standardIcon(QStyle.SP_FileIcon)
        btn_open_img = QAction(open_img_icon, self.tr("Open &Image"), self)

        btn_open_dir.setStatusTip(self.tr("Open a folder to images"))
        btn_open_img.setStatusTip(self.tr("Open an image"))

        btn_open_dir.triggered.connect(self.open_dir)
        btn_open_img.triggered.connect(self.open_img)

        # menu
        menu = self.menuBar()

        # file menu
        file_menu = menu.addMenu(self.tr("&File"))
        file_menu.addAction(btn_open_dir)
        file_menu.addAction(btn_open_img)
        file_menu.addSeparator()
        file_menu.addAction(self.tr("E&xit"), self.close)

        option_menu = menu.addMenu(self.tr("&Options"))
        option_menu.addAction(self.tr("&Preferences"), self.preferences)
        option_menu.addSeparator()

        option_language_menu = option_menu.addMenu(self.tr("&Language"))
        option_language_menu.addAction("&English", self.set_language_en)
        option_language_menu.addAction("&Chinese", self.set_language_cn)

        # help menu
        help_menu = menu.addMenu(self.tr("&Help"))
        help_menu.addAction(self.tr("&Website"), self.open_website)
        help_menu.addAction(self.tr("Show Help (&Markdown)"),
                            self.open_help_markdown)
        help_menu.addAction(self.tr("Show Help (HTML)"), self.open_help_html)
        help_menu.addSeparator()
        help_menu.addAction(self.tr("About"), self.about)

        # status bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

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
                        Config.global_image_path)
        print("detect_img: current image path: " + Config.global_image_path)
        carplate(Config.global_image_path)

    def open_camera(self):
        self.append_log("Opening camera ...")
        print("Opening camera")

    # open image file and update config.global_image_path
    def open_img(self):
        print("Open image")
        self.append_log("Open image")
        selected_img_name, file_type = QFileDialog.getOpenFileName(
            self, "Open Image", filter='Image Files (*.png *.jpg *.jpeg *.bmp *.webp)')
        if selected_img_name == '':
            # open image file failed
            print("Open image failed")
            self.append_log("Open image failed")
            return None
        else:
            print("selected: "+selected_img_name)
            self.append_log("selected: "+selected_img_name)
            Config.global_image_path = selected_img_name
            print("Current image path is: " + Config.global_image_path)
            self.append_log("Current image path is: " +
                            Config.global_image_path)

    # open image file directory
    def open_dir(self):
        print("Opening image file directory")
        self.append_log("Open image file directory")
        selected_dir = QFileDialog.getExistingDirectory(self, "Open Directory")
        if not selected_dir:
            print("Open image directory failed")
            self.append_log("Open image directory failed")
            return None
        else:
            print("selected: "+selected_dir)
            self.append_log("selected: "+selected_dir)
            Config.global_resource_directory = selected_dir
            print("Current image directory is: " +
                  Config.global_resource_directory)
            self.append_log("Current image directory is: " +
                            Config.global_resource_directory)

    def preferences(self):
        pass

    def set_language_en(self):
        print("Set language to English")
        self.append_log("Set language to English")
        Config.global_language = 'en'

    def set_language_cn(self):
        print("Set language to Chinese")
        self.append_log("Set language to Chinese")
        Config.global_language = 'zh'

    def open_help_markdown(self):
        print("Opening help markdown")
        self.append_log("Opening help markdown")
        Utils.openfile_sys(Config.global_help_markdown_path)

    def open_help_html(self):
        print("Opening help html")
        self.append_log("Opening help html")
        Utils.openfile_sys(Config.global_help_html_path)

    def about(self):
        self.setAutoFillBackground(True)
        text = "Car++ is a car plate recognition software."
        text = "<center>" \
            "<h1>Car++</h1>" \
            "&#8291;" \
            "<img src=icon.svg>" \
            "</center>" \
            "<p>Version 0.0.7<br/>" \
            "Copyleft &copy; Jxau Univ.</p>"
        QMessageBox.about(self, "About Car++",
                          text)

    def open_website(self):
        import webbrowser
        webbrowser.open("https://github.com/josedelinux/AutoPlusPlus")

    def findQmFiles(self):
        trans_dir = QDir('translations')
        filename = trans_dir.entryList(['*.qm'], QDir.Files, QDir.Name)
        return [trans_dir.filePath(fn) for fn in filename]


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # update path to absolute path
    Config.global_resource_directory = Utils.update_path(
        Config.global_resource_directory)
    Config.global_image_path = Utils.update_path(Config.global_image_path)
    Config.global_help_html_path = Utils.update_path(
        Config.global_help_html_path)
    Config.global_help_markdown_path = Utils.update_path(
        Config.global_help_markdown_path)

    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    # set up translation
    t = QTranslator()
    if Config.global_language == 'zh':
        t.load("translations/zh.qm")
        app.installTranslator(t)

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
