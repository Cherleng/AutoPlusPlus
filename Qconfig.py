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
configuration
"""


def clear_config():
    """
    clear all configuration, irreversibly
    """
    settings = QSettings("config.ini", QSettings.IniFormat)
    settings.clear()
    settings.sync()
    del settings


def reset_default():
    """
    reset to default configuration, irreversibly
    """
    clear_config()

    updateConfig("lang", "translations/zh.qm")

    updateConfig("RDir", "./Resources/Detection/")

    updateConfig("img", "./Resources/Detection/car20.jpg")


def __init__():
    """
    load all the configuration to global variables
    """
    settings = QSettings("config.ini", QSettings.IniFormat)

    global global_language
    global_language = settings.value("lang")

    global global_resource_directory
    global_resource_directory = settings.value("RDir")

    global global_image_path
    global_image_path = settings.value("img")

    # shouldn't be visible to the user jaja
    global global_progress_bar_interval
    global_progress_bar_interval = 2

    global global_progress_bar_step
    global_progress_bar_step = 2

    import time
    updateConfig("last_access_time", time.asctime())


def updateConfig(key, value):
    """
    update persistent configuration
    create one if key not exist
    """

    current_settings = QSettings("config.ini", QSettings.IniFormat)

    #current_settings.setValue(key, Qconfig.__dict__[key])
    current_settings.setValue(key, value)

    current_settings.sync()
    del current_settings


def test_Qconfig():
    """
    test Qconfig
    """
    import time
    print("test Qconfig")
    last_access_time = time.asctime()
    print("last access time: " + last_access_time)

    # update single configuration
    updateConfig("last_access_time", last_access_time)


if __name__ == "__main__":
    reset_default()
    test_Qconfig()
