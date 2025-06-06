import sys
import os
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QListWidget
)
import torch


class DropListWidget(QListWidget):
    """List widget that accepts drag and drop of files."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addItem(url.toLocalFile())
            event.accept()
        else:
            event.ignore()


class StemGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Stem Splitter")
        layout = QVBoxLayout()

        self.info = QLabel("Drag audio files here or choose a folder")
        layout.addWidget(self.info)

        self.list_widget = DropListWidget()
        layout.addWidget(self.list_widget)

        self.folder_btn = QPushButton("Choose Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        layout.addWidget(self.folder_btn)

        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)

        self.setLayout(layout)

    def choose_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            for name in os.listdir(path):
                if name.lower().endswith((".mp3", ".wav", ".flac", ".ogg")):
                    self.list_widget.addItem(os.path.join(path, name))

    def start_processing(self):
        files = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if not files:
            QtWidgets.QMessageBox.warning(self, "No files", "Add files to process")
            return
        self.process_btn.setEnabled(False)
        thread = threading.Thread(target=self.process_files, args=(files,), daemon=True)
        thread.start()

    def process_files(self, files):
        model_type = self.select_model()
        for file in files:
            self.run_separation(file, model_type)
        QtWidgets.QMessageBox.information(self, "Done", "Processing finished")
        self.process_btn.setEnabled(True)

    def select_model(self):
        """Choose model based on available VRAM."""
        if torch.cuda.is_available():
            vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        else:
            vram = 0
        if vram < 4:
            return "spleeter"
        else:
            return "demucs"

    def run_separation(self, filepath, model_type):
        if model_type == "demucs":
            from demucs.apply import apply_model
            from demucs.pretrained import get_model
            model = get_model("htdemucs")
            apply_model(model, filepath, dest=os.path.join(os.path.dirname(filepath), "stems"))
        else:
            from spleeter.separator import Separator
            separator = Separator("spleeter:2stems")
            separator.separate_to_file(filepath, os.path.join(os.path.dirname(filepath), "stems"))


def main():
    app = QApplication(sys.argv)
    gui = StemGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
