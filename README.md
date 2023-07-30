```diff
! This project is unmaintained.
```
> ### Superceded by 👉 [MediaBro4caddy](https://github.com/glowinthedark/mediabro4caddy)

# PyMediaCenter
A local media browser app for navigating file systems that contain images, audio or video files, and displaying associated content such as PDF, HTML, or TXT. 

The primary use case is viewing audio or video files with associated notes in PDF, HTML or TXT format. VTT and SRT video subtitles are supported. Clicking a media file will open it in the preview panel and search for a matching PDF or HTML file with the same base name. If a matching content file was found it will be loaded in the preview panel below the media panel. You can define custom matching logic by adding the regular expression pair in `config.js`.

For image files thumbnail previews are generated in the left navigation panel which makes it possible to use the app as a gallery viewer.

The app is based on Python's SimpleHTTPServer web server with a browser-based HTML+JS content.

For displaying PDF files the browser must have the corresponding plugins — Chrome and Firefox support PDFs out of the box. For displaying PDF files in Internet Explorer, Adobe Reader or [Foxit Reader plugin](https://help.foxitsoftware.com/kb/how-to-configure-internet-explorer-to-use-foxit-pdf-plugin.php) has to be installed.

#### Features:

* browsing audio, video, text, and images with thumbnail previews
* displaying PDF and HTML content with associated audio/video links
* resizable navigation and content panels
* custom media root folder (by default `/` or `c:\` on windows).
* start/stop media playback on mouse click or on spacebar press.

Example: if a folder contains a PDF file named `lesson-01.pdf` and a video file named `lesson-01.mp4`, then clicking the PDF file will display it in the content panel while the video will start playing in the media panel above.

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

## Usage
1. Clone the repo with `git` or download the zip file and upack.
1. Switch into the folder and run from the terminal:

_to serve from the root folder_
```bash
python3 mediabrowser.py --browser
```

_to set a specific folder as the web root_
```bash
python3 mediabrowser.py /path-to-my-media-folder --browser
```
As an alternative, you can use the provided `Makefile`:

```bash
make run
```

Once the media server is running you can acccess the interface at:

- http://localhost:8088

### Image thumbnails
To enable downscaling of thumbnails the `Pillow` image library needs to be installed:

```bash
pip3 install Pillow
```
