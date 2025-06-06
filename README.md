# AI-Stem-Splitter

A simple GUI for separating audio stems using Demucs or Spleeter.

## Installation

Install Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the GUI application:

```bash
python -m src.gui_app
```

On first launch you'll be asked to select a directory to store the downloaded
Demucs/Spleeter models. Separated tracks for each file are written under a
`stems/` folder inside the chosen output directory.
