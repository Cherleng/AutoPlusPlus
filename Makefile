DATAFLAG = --add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;." --add-data="Resources\\Detection\\car20.jpg;Resources\\Detection\\"

pyinstaller:
	pyinstaller --onedir --windowed main.py ${DATAFLAG}