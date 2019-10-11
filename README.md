# PyMediaCenter
A local media browser app for navigating file systems that contain images, audio or video files, and displaying associated content such as PDF, HTML, or TXT. 

The primary use case is viewing audio or video files with associated notes in PDF, HTML or TXT format. Clicking a media file will open it in the preview panel and search for a matching PDF or HTML file with the same base name. If a matching content file was found it will be loaded in the preview panel below the media panel. You can define custom matching logic by adding the regular expression pair in `config.js`.

For image files thumbnail previews are generated in the left navigation panel which makes it possible to use the app as a gallery viewer.

The app is implemented as a tiny web server that opens a page in your browser with content split into a left navigation  panel, a media panel for video or audio, and a content panel for PDF and HTML.

For displaying PDF files the browser must have the corresponding plugins — Chrome and Firefox support PDFs out of the box. For displaying PDF files in Internet Explorer, Adobe Reader or [Foxit Reader plugin](https://help.foxitsoftware.com/kb/how-to-configure-internet-explorer-to-use-foxit-pdf-plugin.php) must be installed.

#### Features:

* M3U playlist generation for folders with media files
* browsing images with thumbnail previews in the left navigation panel (gallery mode)
* displaying PDF and HTML content with associated audio/video links
* user-defined regular expressions for matching media files to PDF, HTML or text content (`config.js`)
* adjustable playback speed for media files
* resizable navigation and content panels
* auto-open browser window on server start
* custom media root folder can be specified as first argument (by default the system root will be used (e.g. `/` or `c:\` on windows).
* start/stop media playback on mouse click or on spacebar press.

Example: if a folder contains a PDF file named `lesson-01.pdf` and a video file named `lesson-01.mp4`, then clicking the PDF file will display it in the content panel while the video will start playing in the media panel above.

![LocalMediaBrowser](/mediabrowser-sample.png?raw=true "MediaBrowser8088 main window")

## Supported media formats
Playback of media files is handled by the web browser therefore support is limited to the capabilities of the corresponding HTML5 `<audio/>` and `<video/>` elements which currently include: MP3, MP4 audio/video (H.264, AAC, MP3 codecs), MP4 container with Flac codec, OGG audio and video (Theora, Vorbis, Opus, Flac codecs), FLAC, WebM audio/video (VP8, VP9 codecs), WAV (PCM).

For more details refer to [mozilla browser media compatibility table](https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats#Browser_compatibility).

## Keyboard navigation shortcuts

| Key press  | Action |
| ------------- | ------------- |
| Left  | Seek backward 5 sec  |
| Right  | Seek forward 5 sec  |
| Up  | Seek forward 1 min  |
| Down  | Seek backward 1 min  |
| Space  | Pause/Play  |
| f  | Toggle full screen  |

## Download
Prebuilt (possibly outdated) packages for MacOS and Windows can be downloaded from the [Releases](https://github.com/glowinthedark/local-media-browser/releases) section.

To run on Linux follow the Usage steps below.

## Usage (Python 2.x)
1. Clone the repo with `git` or download the zip file and upack.
1. Switch into the folder and run from the terminal:

_to serve from the root folder_
```bash
python mediaserver.py
```

_to set a specific folder as the web root_
```bash
python mediaserver.py /path-to-my-media-folder
```

Once the media server has started it will open a page at the following URL:

http://localhost:8088

## Usage (Python 3.x)
To run under python 3 switch to the `python3` branch with `git checkout python3` and run the server with `python3 mediaserver.py`

### Image thumbnails
To enable downscaling of thumbnails the `Pillow` image library needs to be installed:

```bash
pip install Pillow
```
