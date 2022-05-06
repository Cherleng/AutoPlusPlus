RESFLAG = --add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;." --add-data="Resources\\Detection\\car20.jpg;Resources\\Detection\\"

HELPDATAFLAG = --add-data="Resources\\help.md;Resources\\" --add-data="Resources\\help.html;Resources\\"

pyinstaller:
	pyinstaller --onedir --windowed main.py ${RESFLAG} ${HELPDATAFLAG}

test:
	pyinstaller --onedir  main.py ${RESFLAG} ${HELPDATAFLAG}

updts:
	pylupdate5.exe main.py -ts translations\\zh.ts
	pylupdate5.exe main.py -ts translations\\en.ts

clean:
	rm -rf build dist *.spec