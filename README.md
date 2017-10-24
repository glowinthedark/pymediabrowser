# Local Media Browser
A local media browser app for navigating a file systems that contains images, audio or video files with associated content such as PDF, HTML, or TXT. 

The app is implemented as a local web server that opens a page in your browser with content split into a file navigation side panel, a media panel for video or audio, and a content panel for PDF and HTML.

For displaying PDF files the browser must have the corresponding plugins — Chrome and Firefox support PDFs out of the box. For displaying PDF files in Internet Explorer, Adobe Reader must be installed.

#### Features:

* M3U playlist generation for folders that contain media files
* browsing images with thumbnail previews in the left panel (gallery mode)
* displaying PDF and HTML content with associated audio/video links
* user-defined regular expressions for matching media files to PDF, HTML or text content (`config.js`)
* adjustable playback speed for media files
* resizable navigation and content panels
* auto-open browser window on server start
* custom media root folder can be specified as first argument (by default the system root will be used (e.g. `/` or `c:\` on windows).
* start/stop media playback on click or on spacebar press.

Example: if a folder contains a PDF file named `lesson-01.pdf` and a video file named `lesson-01.mp4`, then clicking the PDF file will display it in the bottom content panel while the video playback will start in the top media panel.

![LocalMediaBrowser](/mediabrowser-sample.png?raw=true "MediaBrowser8088 main window")


## Download
To download prebuilt packages for MacOS and Windows go to the [Releases](https://github.com/elFua/local-media-browser/releases) section.

To run on Linux follow the Usage steps below.

## Usage (Python 2.x)
1. Clone with `git` or download the zip file and upack.
1. Switch into the folder and run from the terminal:

_to serve from the root folder_
```bash
python mediaserver.py
```

_to set the web root to a specific folder_
```bash
python mediaserver.py /path-to-my-media-folder
```

Once the media server is running open the following URL in your web browser:

http://localhost:8088

## Usage (Python 3.x)
To run under python 3 switch to the `python3` branch with `git checkout python3` and run the server with `python3 mediaserver.py`

### Image thumbnails
To enable downscaling of thumbnails the `Pillow` image library needs to be installed:

```bash
pip install Pillow
```
