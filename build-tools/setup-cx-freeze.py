import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],
    "excludes": ['gtk', 'PyQt4', 'PyQt5', 'Tkinter', 'email', 'distutils', 'logging', 'unittest'],
    "include_files":  ['..\\lib\\']}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(name="Media Browser",
      version="0.8088",
      description="Local file system media browser running on http://localhost:8088",
      icon="..\\lib\\ico\\favicon.ico",
      options={"build_exe": build_exe_options},
      executables=[Executable("..\mediaserver.py",
                              shortcutName="MediaBrowser",
                              shortcutDir="DesktopFolder",
                              base=base)])
