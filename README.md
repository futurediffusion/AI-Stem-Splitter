# AI-Stem-Splitter

A simple GUI for separating audio stems using Demucs or Spleeter.

## Requirements

- Python 3.8 or newer
- Optional CUDA enabled GPU (Demucs is automatically chosen when at least
  4&nbsp;GB of VRAM are detected)


## Installation

Install Python packages:

```bash
pip install -r requirements.txt
```

The requirements file pins `numpy<2`, `spleeter==2.4.2` and
`tensorflow==2.12.1` for compatibility. If you already have an existing
environment, recreate it or reinstall the dependencies using the updated
requirements file.

Run these commands from the repository root so that the GUI can import the
package correctly.

## Usage

Run the GUI application on any platform:

```bash
python -m src.gui_app
```

Windows users can also launch the program by double-clicking
`start_app.bat`.
Double-clicking the script will create a virtual environment on the first run
and reuse it on subsequent launches.

On first launch you'll be asked to select a directory to store the downloaded
Demucs/Spleeter models. Separated tracks for each file are written under a
`stems/` folder inside the chosen output directory. By default the models and
output are stored inside the repository under `models/` and `output/`.

The GUI accepts MP3, WAV, FLAC and OGG files. The application can run entirely
on the CPU, or it will use the GPU when one is available. It has been tested on
GPUs with up to 8&nbsp;GB of VRAM.
