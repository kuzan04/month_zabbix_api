w-install:
	python -m venv .dataenv
	call .dataenv\Scripts\activate
	pip install dotenv statistics requests python-dateutil pyinstaller
	
install:
	python -m venv .dataenv
	source .dataenv/bin/activate
	pip install dotenv statistics requests python-dateutil pyinstaller

w-builds:
	pyinstaller --onefile --name="report-zabbix" --icon=icons/myicon.ico --version-file="version.txt" --hidden-import=dotenv --add-data=".env;." main.py
builds:
	pyinstaller --onefile --name="report-zabbix" --version-file="version.txt" --hidden-import=dotenv --add-data=".env:." main.py
	#--icon=icons/myicon.ico

disable:
	deactivate
