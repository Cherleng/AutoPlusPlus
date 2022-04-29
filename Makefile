RESFLAG = --add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;." --add-data="Resources\\Detection\\car20.jpg;Resources\\Detection\\"

HELPDATAFLAG = --add-data="Resources\\help.md;Resources\\" --add-data="Resources\\help.html;Resources\\"

pyinstaller:
	pyinstaller --onedir --windowed main.py ${RESFLAG} ${HELPDATAFLAG}

test:
	pyinstaller --onedir  main.py ${RESFLAG} ${HELPDATAFLAG}

clean:
	rm -rf build dist *.spec