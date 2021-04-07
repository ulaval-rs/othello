import os
import shutil
from distutils.command.build import build


class CleanBuild(build):

    def run(self):
        # Removing unused libs
        libs_paths = [os.path.join('build', build_dir, 'lib') for build_dir in os.listdir('build')]
        for project_lib_path in libs_paths:
            shutil.rmtree(os.path.join(project_lib_path, 'test'))
            shutil.rmtree(os.path.join(project_lib_path, 'unittest'))

            shutil.rmtree(os.path.join(project_lib_path, 'PySide2', 'examples'))
            shutil.rmtree(os.path.join(project_lib_path, 'PySide2', 'glue'))
            shutil.rmtree(os.path.join(project_lib_path, 'PySide2', 'qml'))
            shutil.rmtree(os.path.join(project_lib_path, 'PySide2', 'plugins'))
            shutil.rmtree(os.path.join(project_lib_path, 'PySide2', 'translations'))
            os.remove(os.path.join(project_lib_path, 'PySide2', 'Qt5WebEngineCore.dll'))


