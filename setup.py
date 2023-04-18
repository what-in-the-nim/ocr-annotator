from setuptools import setup, find_packages

setup(
    name='nimocr',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        "numpy==1.24.2",
        "opencv_python==4.7.0.72",
        "pandas==2.0.0",
        "Pillow==9.5.0",
        "PyQt6==6.5.0",
        "setuptools==67.6.1"
    ],
    entry_points={
        'console_scripts': [
            'nimocr=nimocr.annotator:run',
        ],
    },
    author='Chatcharin Sangbutsarakum',
    author_email='chatcharinsang@gmail.com',
    description='OCR Annotator Tool',
    url='https://github.com/what-in-the-nim/ocr-annotator',
)
