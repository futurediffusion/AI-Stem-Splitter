import sys
import os
import threading
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QListWidget, QProgressBar,
)
import torch
from .config import Config


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
        self.config = Config()
        layout = QVBoxLayout()

        self.info = QLabel("Drag audio files here or choose a folder")
        layout.addWidget(self.info)

        self.list_widget = DropListWidget()
        layout.addWidget(self.list_widget)

        self.folder_btn = QPushButton("Choose Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        layout.addWidget(self.folder_btn)

        self.model_dir_btn = QPushButton("Set Model Directory")
        self.model_dir_btn.clicked.connect(self.choose_model_dir)
        layout.addWidget(self.model_dir_btn)

        self.output_dir_btn = QPushButton("Set Output Directory")
        self.output_dir_btn.clicked.connect(self.choose_output_dir)
        layout.addWidget(self.output_dir_btn)

        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.log_widget = QListWidget()
        layout.addWidget(self.log_widget)

        self.setLayout(layout)

    def choose_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            for name in os.listdir(path):
                if name.lower().endswith((".mp3", ".wav", ".flac", ".ogg")):
                    self.list_widget.addItem(os.path.join(path, name))

    def choose_model_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Model Directory", self.config.model_dir)
        if path:
            self.config.model_dir = path

    def choose_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.config.output_dir)
        if path:
            self.config.output_dir = path

    def start_processing(self):
        files = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if not files:
            QtWidgets.QMessageBox.warning(self, "No files", "Add files to process")
            return
        self.progress_bar.setMaximum(len(files))
        self.progress_bar.setValue(0)
        self.process_btn.setEnabled(False)
        thread = threading.Thread(target=self.process_files, args=(files,), daemon=True)
        thread.start()

    def process_files(self, files):
        model_type = self.select_model()
        for idx, file in enumerate(files, 1):
            self.log_widget.addItem(f"Processing {Path(file).name}")
            self.run_separation(file, model_type)
            self.progress_bar.setValue(idx)
        QtWidgets.QMessageBox.information(self, "Done", "Processing finished")
        self.process_btn.setEnabled(True)
        self.log_widget.addItem("Finished")

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
        dest = self._make_dest(filepath)
        os.environ.setdefault("HF_HOME", self.config.model_dir)
        os.environ.setdefault("MODEL_PATH", self.config.model_dir)
        if model_type == "demucs":
            from demucs.apply import apply_model
            from demucs.pretrained import get_model
            model = get_model("htdemucs")
            apply_model(model, filepath, dest=dest)
        else:
            from spleeter.separator import Separator
            separator = Separator("spleeter:2stems")
            separator.separate_to_file(filepath, dest)

    def _make_dest(self, filepath: str) -> str:
        base = Path(filepath).stem
        dest = Path(self.config.output_dir) / "stems" / base
        dest.mkdir(parents=True, exist_ok=True)
        return str(dest)


def main():
    app = QApplication(sys.argv)
    gui = StemGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
