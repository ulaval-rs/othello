import sys
from cx_Freeze import setup, Executable

from scripts.clean_build import CleanBuild

build_exe_options = {
    'excludes': [
        'tkinter',
        'sqlite3',
        'pytest',
        'PySide2.QtSql',
        'PySide2.QtScript',
        'PySide2.QtScriptTools',
        'PySide2.QtNetwork',
        'PySide2.Qt3DAnimation',
        'PySide2.Qt3DCore',
        'PySide2.Qt3DExtras',
        'PySide2.Qt3DInput',
        'PySide2.Qt3DLogic',
        'PySide2.Qt3DRender',
        'PySide2.QtAxContainer',
        'PySide2.QtCharts',
        'PySide2.QtDataVisualization',
        'PySide2.QtLocation',
        'PySide2.QtMultimedia',
        'PySide2.QtMultimediaWidgets',
        'PySide2.QtOpenGL',
        'PySide2.QtOpenGLFunctions',
        'PySide2.QtSensors',
        'PySide2.QtWebChannel',
        'PySide2.QtWebEngine',
        'PySide2.QtWebEngineCore',
        'PySide2.QtWebEngineWidgets',
        'PySide2.QtWebSockets',
    ]
}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name='othello',
    version='0.1',
    description='Tools that allow you to read and manipulate M-MACBETH files and transform GIS data accordingly.',
    options={'build_exe': build_exe_options},
    executables=[Executable('othello/othello.py', base=base)],
    cmdclass={
        'clean_build': CleanBuild,
    }
)
