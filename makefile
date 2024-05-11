compile:
	pyinstaller --noconfirm --onefile --windowed --clean --add-data="assets/:." "annotator.py"
