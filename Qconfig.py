__author__ = " Guixin Chen <Valentinofreeman@163.com>"
__credits__ = ["Guixin Chen", "Jiehuang Liu",  "Mingkang Chen",
               "Shuailei Zhao", "HanZhen Fu"]
__license__ = "MIT"
__version__ = "0.0.8"
__maintainer__ = "Guixin Chen, Jiehuang Liu "
__email__ = "Valentinofreeman@163.com"
__status__ = "Prototype"

from PyQt5.QtCore import QSettings, QPoint


"""
配置文件
configuration
"""


def __init__():
    # 全局配置文件
    settings = QSettings("config.ini", QSettings.IniFormat)

    settings.beginGroup("language")

    # 默认语言
    global global_language
    global_language = "zh"

    settings.endGroup()

    settings.beginGroup("resource")
    # 默认目录位置
    global global_resource_directory
    global_resource_directory = settings.value("global_resource_directory", "")
    global_resource_directory = "./Resources/Detection/"

    # 默认图片路径
    global global_image_path
    global_image_path = './Resources/Detection/car20.jpg'
    settings.endGroup()

    # 进度条脉冲间隔
    global global_progress_bar_interval
    global_progress_bar_interval = 2

    # 进度条步长
    global global_progress_bar_step
    global_progress_bar_step = 2

    # help file
    global global_help_markdown_path
    global_help_markdown_path = "./Resources/help.md"

    global global_help_html_path
    global_help_html_path = "./Resources/help.html"
