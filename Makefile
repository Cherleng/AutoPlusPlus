# makefile for the project
RESFLAG =	\
--add-data="Resources\\splashscr_864.png;Resources\\"  --add-data="style.qss;."	\
--add-data="Resources\\Detection\\car20.png;Resources\\Detection\\"	\
--add-data="Resources\\Detection\\car16.jpg;Resources\\Detection\\"	\
--add-data="Resources\\open_img.png;Resources\\" \
--add-data="Resources\\about.jpg;Resources\\" \
--add-data="Resources\\haarcascade_licence_plate.xml;Resources\\" \
--add-data="refer1\\;refer1\\" \
--add-data="config.ini;." \

HELPDATAFLAG = --add-data="Resources\\help.md;Resources\\" \
--add-data="Resources\\help.html;Resources\\" \

TSDATAFLAG = --add-data="translations\\*.qm;translations\\"

ICONDATAFLAG = --add-data="Resources\\*.ico;Resources\\"

pyinstaller:updts
	pyinstaller --onedir --windowed main.py ${RESFLAG} ${HELPDATAFLAG} ${TSDATAFLAG} ${ICONDATAFLAG}

debug:
	pyinstaller --onedir  main.py ${RESFLAG} ${HELPDATAFLAG} ${TSDATAFLAG} ${ICONDATAFLAG}

updts:
	pylupdate5.exe main.py  -noobsolete -ts translations\\zh.ts
	pylupdate5.exe main.py  -noobsolete -ts translations\\en.ts
	pylupdate5.exe main.py  -noobsolete -ts translations\\es.ts

genpref:
	pyuic5.exe preferences.ui -o ui_preferences.py

releasets:updts
	lrelease translations\\*.ts

clean:
	rm -rf build dist *.spec
