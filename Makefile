w-builds:
	pyinstaller --onefile --windowed --name="report-zabbix" --icon=icons/myicon.ico --version-file="version.txt" --hidden-import=dotenv --add-data=".env;." main.py
builds:
	pyinstaller --onefile --windowed --name="report-zabbix" --version-file="version.txt" --hidden-import=dotenv --add-data=".env:." main.py
	#--icon=icons/myicon.ico
