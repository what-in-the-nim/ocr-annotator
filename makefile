compile:
	pyinstaller --noconfirm --onefile --windowed --clean --add-data "assets/logo.png;." "annotator.py"