import os
import sys

import qdarktheme
import pillow_heif

from PIL import Image

from PyQt5.QtWidgets import (
    QDesktopWidget, QFileDialog, QGridLayout, QGroupBox, QMainWindow,
    QApplication, QPushButton, QWidget
)


class MainWindow(QMainWindow):
    def __init__(self, parent = None,) -> None:
        super().__init__(parent)
        self.setWindowTitle("Heng")
        self.resize(960, 540)
        self.setContentsMargins(20, 13, 20, 20)
        self.setStyleSheet("QMainWindow{background: #A7BDD9}")

        self.setCentralWidget(self._main_menu())
        self._center_window()

    def _center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _main_menu(self) -> QWidget:
        group = QGroupBox()
        layout = QGridLayout()

        select_files = QPushButton("Select Photos", group)
        select_files.clicked.connect(self._get_file)

        layout.addWidget(select_files)

        group.setLayout(layout)
        group.setStyleSheet(
            """
            QGroupBox {
                background: #F0F2F2;
                border: 0;
            }
            """
        )
        return group

    def _get_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.exec()

        selected_files = dialog.selectedFiles() 
        if selected_files:
            print(dialog.selectedFiles())

    def heif_to_png(self):
        for file in os.listdir("FOTO/"):
            heif_file = pillow_heif.read_heif(f"FOTO/{file}")
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
            image.save(f"./convert/{file[:len(file) - 5]}.png", format("png"))

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
