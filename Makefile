DATAFLAG = --add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;."

pyinstaller:
	pyinstaller --onefile --windowed main.py ${DATAFLAG}