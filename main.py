import os
import sys
import time
from PyQt5 import QtCore, QtGui

import qdarktheme
import pillow_heif

from PIL import Image

from PyQt5.QtWidgets import (
    QDesktopWidget, QDialog, QFileDialog,
    QGridLayout, QGroupBox, QLabel, QMainWindow,
    QApplication, QProgressBar, QPushButton, QTextEdit,
    QWidget
)

class PopUpDialog(QDialog):
    def __init__(self, parent: QWidget, title: str, message: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        
        label = QLabel(message, self)
        layout = QGridLayout()

        layout.addWidget(label)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, parent = None,) -> None:
        super().__init__(parent)
        self.setWindowTitle("Heng")
        self.resize(960, 540)
        self.setContentsMargins(20, 13, 20, 20)
        self.setStyleSheet("QMainWindow{background: #A7BDD9}")

        self.output_dir = None

        self.setCentralWidget(self._main_menu())
        self._center_window()

    def _center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _logs_group(self) -> QWidget:
        group = QGroupBox()
        layout = QGridLayout()

        self.logs = QTextEdit()

        layout.addWidget(self.logs)
        group.setLayout(layout)
        group.setTitle("Logs")
        group.setStyleSheet(
            """
            QGroupBox {
                background: #F0F2F2;
            }
            """
        )
        return group

    def _main_menu(self) -> QWidget:
        group = QGroupBox()
        layout = QGridLayout()

        select_files = QPushButton("Select Photos", group)
        select_files.clicked.connect(self._get_file)

        select_output_dir = QPushButton("Select Output Folder", group)
        select_output_dir.clicked.connect(self._set_output_dir)

        open_dir = QPushButton("Open Output Folder", group)
        open_dir.clicked.connect(self._open_output_dir)

        self.prog_bar = QProgressBar()

        layout.addWidget(select_output_dir, 0, 0)
        layout.addWidget(select_files, 0, 1)
        layout.addWidget(open_dir, 0, 2)

        layout.addWidget(self.prog_bar, 1, 0, 1, 3)
        layout.addWidget(self._logs_group(), 2, 0, 1, 3)

        group.setLayout(layout)
        group.setAccessibleName("GroupBox1")
        group.setStyleSheet(
            """
            QGroupBox1 {
                background: #F0F2F2;
                border: 0;
            }
            """
        )
        return group

    def _open_output_dir(self):
        if self.output_dir:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.output_dir))
        else:
            PopUpDialog(self, "Error", "Error: please chose output folder...").exec()

    def _set_output_dir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.exec()

        self.logs.append(f"SET OUTPUT FOLDER: {dialog.selectedFiles()[0]}")
        self.output_dir = dialog.selectedFiles()[0] 

    def _get_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.exec()

        selected_files = dialog.selectedFiles() 
        if selected_files:
            self.prog_bar.setMaximum(len(selected_files))
            self.logs.append(f"Total photos: {len(selected_files)}")
            time.sleep(0.5)
            self.heif_to_png(selected_files)

    def heif_to_png(self, files: list[str]):
        if not self.output_dir:
            PopUpDialog(self, "Error", "Error: please chose output folder...").exec()
            return

        for idx,file in enumerate(files, 1):

            # Skip not supported format
            if not file.endswith((".heic", ".HEIC", ".heif", ".HEIF")):
                self.logs.append(f"skip: {file}")
                continue

            self.logs.append(f"converting: {file}")

            heif_file = pillow_heif.read_heif(file)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
            output = file.split("/")
            image.save(f"{self.output_dir}/{output[-1][:len(file) - 5]}.png", format("png"))

            self.prog_bar.setValue(idx)

        PopUpDialog(self, "Success", "Success convert all the files").exec()

def main():
    """
    Creating entry point
    """

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication([])
    ex = MainWindow()

    ex.show()
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
