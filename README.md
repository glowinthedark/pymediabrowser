# Local Media Browser
A minimalistic local media browser for navigating a local file system that contains audio or video files with associated content such as PDF, HTML, or TXT.

For example, if a folder contains a video file named `lesson-01.mp4` and a PDF file named `lesson-01.pdf` then clicking either of the files will load both files in the corresponding panels on the page so that you can listen or watch the video while reading the PDF notes side-by-side.

## Usage (Python 2.x)
1. Clone or download zip and upack.
1. Switch into the folder and run from the terminal:

_to serve from the current folder_
```bash
python mediaserver.py
```

_to serve a specific folder_
```bash
python mediaserver.py /mymediafolder
```

## Usage (Python 3.x)
To run under python 3 switch to the `python3` branch with `git checkout python3` and run the server with `python3 mediaserver.py`
