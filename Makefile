w-install:
	python -m venv .dataenv
	call .dataenv\Scripts\activate
	pip install dotenv statistics requests
	
install:
	python -m venv .dataenv
	source .dataenv/bin/activate
	pip install dotenv statistics requests

w-builds:
	pyinstaller --onefile --windowed --name="report-zabbix" --icon=icons/myicon.ico --version-file="version.txt" --hidden-import=dotenv --add-data=".env;." main.py
builds:
	pyinstaller --onefile --windowed --name="report-zabbix" --version-file="version.txt" --hidden-import=dotenv --add-data=".env:." main.py
	#--icon=icons/myicon.ico

disable:
	deactivate
