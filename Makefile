RESFLAG =	\
--add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;."	\
--add-data="Resources\\Detection\\car20.jpg;Resources\\Detection\\" \
--add-data="Resources\\open_img.png;Resources\\" \
--add-data="Resources\\about.jpg;Resources\\" 

HELPDATAFLAG = --add-data="Resources\\help.md;Resources\\" --add-data="Resources\\help.html;Resources\\"

TSDATAFLAG = --add-data="translations\\*.qm;translations\\"

ICONDATAFLAG = --add-data="Resources\\*.ico;Resources\\"

pyinstaller:
	pyinstaller --onedir --windowed main.py ${RESFLAG} ${HELPDATAFLAG} ${TSDATAFLAG} ${ICONDATAFLAG}

test:
	pyinstaller --onedir  main.py ${RESFLAG} ${HELPDATAFLAG} ${TSDATAFLAG} ${ICONDATAFLAG}

updts:
	pylupdate5.exe main.py  -noobsolete -ts translations\\zh.ts
	pylupdate5.exe main.py  -noobsolete -ts translations\\en.ts

clean:
	rm -rf build dist *.spec