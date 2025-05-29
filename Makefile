w-install:
	python -m venv .dataenv
	.dataenv\Scripts\pip install - requirements.txt
	
install:
	@python -m venv .dataenv
	.dataenv/bin/pip install -r requirements.txt

w-builds:
	pyinstaller --onefile --name="report-zabbix" --icon=icons/myicon.ico --version-file="version.txt" --hidden-import=dotenv --add-data=".env;." main.py
builds:
	pyinstaller --onefile --name="report-zabbix" --version-file="version.txt" --hidden-import=dotenv --add-data=".env:." main.py
	#--icon=icons/myicon.ico

disable:
	 deactivate

dev:
	.dataenv/bin/python main.py
