from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QFileDialog, QDialog, QMessageBox
from PyQt5.QtCore import *
import sys
import os

class utilityGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_folder = ''
        self.setup_file = ''
        self.output_folder = ''

    def startUtility(self):
        """ Run IntuneWinAppUtil.exe with the specified settings"""
        setup_folder = self.setup_folder
        setup_file = self.setup_file
        output_folder = self.output_folder

        if os.path.isfile('.\IntuneWinAppUtil.exe'):
            if self.setup_folder and self.setup_file and self.output_folder:
                print(f"Setup folder:\t{setup_folder}") # dbg
                print(f"Setup file:\t{setup_file}") # dbg
                print(f"Output folder:\t{output_folder}") # dbg
                print(f"Running:\t.\IntuneWinAppUtil.exe -q -c {setup_folder} -s {setup_file} -o {output_folder}")

                out_filepath = os.path.join(output_folder, (os.path.split(setup_file)[-1].split(".")[0] + ".intunewin")).replace("/", "\\")
                os.system(f".\IntuneWinAppUtil.exe -q -c {setup_folder} -s {setup_file} -o {output_folder}")
                QMessageBox.about(self, "Done", f"IntuneWIN file created:\n{out_filepath}")
            else:
                QMessageBox.about(self, "Error", "Please specify all paths.")
        else:
            QMessageBox.about(self, "Error", "IntuneWinAppUtil.exe not found.\n\nPlease download it and add it to this directory.\nhttps://github.com/Microsoft/Intune-Win32-App-Packaging-Tool")
    
    def initUI(self):
        # GUI width/height ==================================================================================== #
        max_width = 550
        max_height = 270

        # Build the window widget
        self.setGeometry(300, 300, max_width, max_height)  # x, y, w, h
        self.setWindowTitle("IntuneWIN App Packaging utility")
        self.center()

        # Add a label
        label = QLabel("IntuneWIN App Packaging Utility", self)
        label.resize(label.sizeHint())
        label.move(20, 20)
        
        # Select setup folder ================================================================================= #
        label = QLabel("Select setup folder:", self)
        label.resize(label.sizeHint())
        label.move(20,45)
        label.setToolTip('end file 1')

        select_setup_folder = QPushButton('Select setup folder', self)
        select_setup_folder.resize((max_width - 40), 28)
        select_setup_folder.move(20, 65)
        select_setup_folder.clicked.connect(self.selectSetupFolder)

        # Select setup file =================================================================================== #
        label = QLabel("Select setup file:", self)
        label.resize(label.sizeHint())
        label.move(20,100)
        label.setToolTip('end file 1')

        select_setup_file = QPushButton('Select setup file', self)
        select_setup_file.resize((max_width - 40), 28)
        select_setup_file.move(20, 120)
        select_setup_file.clicked.connect(self.selectSetupFile)

        # Select output folder ================================================================================ #
        label = QLabel("Select output folder:", self)
        label.resize(label.sizeHint())
        label.move(20,155)
        label.setToolTip('end file 1')

        select_output_folder = QPushButton('Select output folder', self)
        select_output_folder.resize((max_width - 40), 28)
        select_output_folder.move(20, 175)
        select_output_folder.clicked.connect(self.selectOutputFolder)

        # run ================================================================================================= #
        btn_start = QPushButton('Run', self)
        btn_start.move(20, 213)
        btn_start.clicked.connect(self.startUtility)

        self.statusBar()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selectSetupFile(self):
        """ Get path to the setup file """
        if self.setup_folder:
            dialog = QFileDialog(self)
            dialog.setWindowTitle('Select executable')
            dialog.setNameFilter('Executable files (*.exe)')
            dialog.setDirectory(self.setup_folder)
            dialog.setFileMode(QFileDialog.ExistingFile)

            if dialog.exec_() == QDialog.Accepted:
                file_full_path = str(dialog.selectedFiles()[0])
                self.setup_file = str(dialog.selectedFiles()[0])
            else:
                return None
        else:
            QMessageBox.about(self, "Error", "Please specify setup folder first.")

    def selectSetupFolder(self):
        """ Get path to the setup folder """
        starting_dir = QDir.rootPath()
        self.setup_folder = QFileDialog().getExistingDirectory(None, 'Open working directory', starting_dir, QFileDialog.ShowDirsOnly)
    
    def selectOutputFolder(self):
        """ Get path to the output folder """
        starting_dir = QDir.rootPath()
        self.output_folder = QFileDialog().getExistingDirectory(None, 'Open working directory', starting_dir, QFileDialog.ShowDirsOnly)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = utilityGUI()
    sys.exit(app.exec_())
