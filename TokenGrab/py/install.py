import os

modules = [
    "requests",
    "Crypto",
    "pycryptodome",
    "pywin32",
    "tkinter",
    "pyinstaller"
]

os.system("pip install --upgrade pip")

for module in modules:
    os.system(f"pip install {module}")
