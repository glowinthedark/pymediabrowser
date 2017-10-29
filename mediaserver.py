#!/usr/bin/env python
# coding=utf-8

#  Copyright (c) 2017 booleanbaby
#  Released under the MIT license

# - automatically find matching audio/video or PDF file for clicked file
# - resize split panels with mouse
# - start/stop media with spacebar or mouse/click
# - select playback speed for video/audio
# - http range support

# Thanks to:
# Dan Vanderkam for RangeHTTPServer - https://github.com/danvk/RangeHTTPServer
#
import argparse
import re
import socket
import webbrowser
from string import Template
from urllib import quote, unquote
import SocketServer
import cgi
import os
import platform
import posixpath
import sys
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from StringIO import StringIO
try:
    from PIL import Image
except ImportError:
    Image = None

# https://emojipedia.org/

VERSION = '8088.11'

DEFAULT_PORT = 8088

ICON_AUDIO = "&#x1F3A7;"
ICON_VIDEO = "&#x1F3A5;"
ICON_PDF = "&#128195;"
ICON_DIR = "&#128193;"
ICON_HTML = "&#x1F30D;"
ICON_IMAGE = "&#xFE0F;"
ICON_UNKNOWN = "&#x2753;"
ICON_BACK = "&#x21B0;"
ICON_TEXT = "&#x1F4C3;"

icons_by_type = {
    '.pdf': ICON_PDF,
    '.mp3': ICON_AUDIO,
    '.mp4': ICON_VIDEO,
    '.m4v': ICON_VIDEO,
    '.mov': ICON_VIDEO,
    '.3gp': ICON_VIDEO,
    '.3gpp': ICON_VIDEO,
    '.webm': ICON_VIDEO,
    '.html': ICON_HTML,
    '.jpg': ICON_IMAGE,
    '.jpeg': ICON_IMAGE,
    '.png': ICON_IMAGE,
    '.gif': ICON_IMAGE,
    '.webp': ICON_IMAGE,
    '.txt': ICON_TEXT,
    '.srt': ICON_TEXT,
    '.ini': ICON_TEXT,
    '.cfg': ICON_TEXT,
    '.conf': ICON_TEXT,
    '.vimrc': ICON_TEXT,
    '.bashrc': ICON_TEXT,
}

# bytes in a megabyte; for displaying friendly file sizes
MBFACTOR = float(1 << 20)

MEDIALIST_M3U = 'medialist.m3u'
IMG_THUMBNAIL_SELECTOR = '?mediabro-thumb.jpg'

REGEX_BYTE_RANGE = re.compile(r'bytes=(\d+)-(\d+)?$')
REGEX_INTERNAL_FILE = re.compile("^/lib/(css|js|ico)/.*\.(css|js|png|ico|xml|json)$", re.IGNORECASE)
REGEX_MEDIA_FILE = re.compile("\.(3gp|3gpp|aac|aiff|avi|mov|mp1|mp2|mp3|mp4|m4a|flac|m4v|mpeg|mpg|oga|ogg|ogv|ogm|wav|webm|wma|wmv)$", re.IGNORECASE)
REGEX_IMAGE_FILE = re.compile("\.(gif|jpg|jpeg|apng|png|tif|tiff|bmp|eps|pcx|webp|ico|icns|psd|xpm|wmf)$", re.IGNORECASE)


def get_script_dir():
    if getattr(sys, 'frozen', False):
        # frozen
        dir_ = os.path.dirname(sys.executable)
    else:
        # unfrozen
        dir_ = os.path.dirname(os.path.realpath(__file__))
    return dir_


def open_url_in_browser(url):
    # webbrowser.open() is partially broken in OSX Sierra v10.12.5 and fixed in v10.12.6
    # (https://bugs.python.org/issue30392)
    if sys.platform == 'darwin':
        for name in ('chrome', 'google-chrome', 'safari'):
            try:
                controller = webbrowser.get(name)
                controller.open_new_tab(url)
                return
            except Exception as e:
                print(e)
    else:
        webbrowser.open_new_tab(url)


def make_thumbnail(image_path, size):
    img = Image.open(image_path)
    ''':type : PIL.Image'''

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(size)
    img_io = StringIO()
    img.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    return img_io.getvalue()


class MyRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.media_root_dir = args.webroot
        template_path = os.path.join(get_script_dir(), "lib", "mediabro.html")

        html_content = open(template_path).read()

        self.page_template = Template(html_content)

        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    """Adds support for HTTP 'Range' requests to SimpleHTTPRequestHandler

    The approach is to:
    - Override send_head to look for 'Range' and respond appropriately.
    - Override copyfile to only transmit a range when requested.
    """
    def send_head(self):
        if 'Range' not in self.headers:
            self.range = None
            return SimpleHTTPRequestHandler.send_head(self)
        try:
            self.range = self.parse_byte_range(self.headers['Range'])
        except ValueError as e:
            self.send_error(400, 'Invalid byte range')
            return None
        first, last = self.range

        # Mirroring SimpleHTTPServer.py here
        path = self.translate_path(self.path)
        f = None
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, 'File not found')
            return None

        fs = os.fstat(f.fileno())
        file_len = fs[6]
        if first >= file_len:
            self.send_error(416, 'Requested Range Not Satisfiable')
            return None

        self.send_response(206)
        self.send_header('Content-type', ctype)
        self.send_header('Accept-Ranges', 'bytes')

        if last is None or last >= file_len:
            last = file_len - 1
        response_length = last - first + 1

        self.send_header('Content-Range',
                         'bytes %s-%s/%s' % (first, last, file_len))
        self.send_header('Content-Length', str(response_length))
        self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f


    #  START BYTE RANGE SUPPORT (https://github.com/danvk/RangeHTTPServer)

    def copyfile(self, source, outputfile):
        if not self.range:
            return SimpleHTTPRequestHandler.copyfile(self, source, outputfile)

        # SimpleHTTPRequestHandler uses shutil.copyfileobj, which doesn't let
        # you stop the copying before the end of the file.
        start, stop = self.range  # set in send_head()
        self.copy_byte_range(source, outputfile, start, stop)

    def copy_byte_range(self, infile, outfile, start=None, stop=None, bufsize=16 * 1024):
        """Like shutil.copyfileobj, but only copy a range of the streams.

        Both start and stop are inclusive.
        """
        if start is not None: infile.seek(start)
        while 1:
            to_read = min(bufsize, stop + 1 - infile.tell() if stop else bufsize)
            buf = infile.read(to_read)
            if not buf:
                break
            outfile.write(buf)


    def parse_byte_range(self, byte_range):
        """Returns the two numbers in 'bytes=123-456' or throws ValueError.

        The last number or both numbers may be None.
        """
        if byte_range.strip() == '':
            return None, None

        m = REGEX_BYTE_RANGE.match(byte_range)
        if not m:
            raise ValueError('Invalid byte range %s' % byte_range)

        first, last = [x and int(x) for x in m.groups()]
        if last and last < first:
            raise ValueError('Invalid byte range %s' % byte_range)
        return first, last

    # END BYTE RANGE SUPPORT

    def do_GET(self):

        print(self.path)
        print(self.version_string())

        absolute_path = os.path.join(self.media_root_dir, unquote(self.path[1:]))

        if absolute_path.endswith(MEDIALIST_M3U):
            data = self.generate_m3u(absolute_path)
            self.send_response(200)
            self.send_header("Content-type", "audio/mpegurl")
            self.send_header("Content-length", len(data))
            self.end_headers()
            self.wfile.write(data)
            return

        if IMG_THUMBNAIL_SELECTOR in absolute_path and Image:
            real_image_path = absolute_path.replace(IMG_THUMBNAIL_SELECTOR, '')
            thumbnail_binary = make_thumbnail(real_image_path, (300, 200))
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.send_header("Content-length", len(thumbnail_binary))
            self.end_headers()
            self.wfile.write(thumbnail_binary)
            return

        if not os.path.isdir(absolute_path):
            return SimpleHTTPRequestHandler.do_GET(self)

        response_data = self.get_directory_listing()
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-length", len(response_data))
        self.end_headers()
        self.wfile.write(response_data)

    def get_directory_listing(self):

        translated_path = self.translate_path(self.path)

        entries = self.__list_directory(translated_path)

        if entries:

            app_config = os.path.join(get_script_dir(), "config.js")

            if os.path.exists(app_config):
                custom_replacements = open(app_config).read()
            else:
                custom_replacements = 'URL_TRANSFORMATIONS = [];\n'

            return self.page_template.safe_substitute(file_list=entries, custom_url_transformations=custom_replacements)

    def __list_directory(self, path):
        """
        ***COPIED FROM python standard lib***
        Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        # sort file list with folders first
        list.sort(key=lambda a: (not os.path.isdir(os.path.join(path, a)), a.lower()))
        result = ['''
    <nav>
        <div class="inlined btn-back">
            <a title="parent folder" href="..">{}</a>
        </div>
        <div class="inlined m3u">
            <a target="_blank" href="{}">M3U</a>
        </div>
    </nav>
    <div style="clear:both"></div>
<ul>'''.format(ICON_BACK, MEDIALIST_M3U)]

        for file_entry in list:
            fullname = os.path.join(path, file_entry)
            displayname = linkname = file_entry
            # Append / for directories or @ for symbolic links
            is_dir = os.path.isdir(fullname)

            if is_dir:
                displayname = file_entry + "/"
                linkname = file_entry + "/"
            if os.path.islink(fullname):
                displayname = file_entry + "@"
                # Note: a link to a directory displays with @ and links with /
            quoted_link = quote(linkname)

            _, extension = os.path.splitext(fullname)
            icon = (is_dir and ICON_DIR) or icons_by_type.get(extension.lower(), ICON_UNKNOWN)

            file_type_marker = 'data-type="{type}"'.format(type=is_dir and 'dir' or 'file')

            if icon:
                displayname = "{}&nbsp;{}".format(icon, cgi.escape(displayname))

            size_info = ""
            image_preview = ""
            title = displayname

            if not is_dir:
                size = get_file_size(fullname)

                title = "{} [{}]".format(displayname, size)

                if not args.suppress_size:
                    size_info = '<span class="size">{}</span>'.format(size)

            if re.search(REGEX_IMAGE_FILE, file_entry):
                image_preview = '''<img class="preview" src="{link}{selector}">'''.format(
                    link=quoted_link,
                    selector=IMG_THUMBNAIL_SELECTOR)

            result.append('<li><a {type} title="{title}" href="{link}">{preview}{name}</a>{size_info}\n'.format
                          (type=file_type_marker,
                           title=title,
                           link=quoted_link,
                           preview=image_preview,
                           name=displayname,
                           size_info=size_info))

        return '\n'.join(result)

    def __list_directory_bare(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        # sort file list with folders first
        list.sort(key=lambda a: (not os.path.isdir(os.path.join(path, a)), a.lower()))
        result = []

        domain = args.domain

        # for M3U playlists use the LAN IP
        if domain.startswith('0.') or domain.startswith('127.'):
            domain = get_ip_address()

        m3u_webroot = self.media_root_dir

        for file_entry in list:
            fullname = os.path.join(path, file_entry)
            if m3u_webroot == '/':
                path_relative_to_webroot = fullname
            else:
                path_relative_to_webroot = fullname.replace(m3u_webroot, "")

            result.append((cgi.escape(file_entry), "http://{}:{}{}".format(domain, args.port, quote(path_relative_to_webroot))))

        return result

    @staticmethod
    def is_local_support_file(peth):
        return REGEX_INTERNAL_FILE.match(peth) is not None

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(unquote(path))
        words = path.split('/')
        words = filter(None, words)

        #   for support files need to always use current script dir
        if self.is_local_support_file(path):
            path = get_script_dir()
        else:
            path = self.media_root_dir

        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def generate_m3u(self, path):

        path = path.replace(MEDIALIST_M3U, "")

        entries = self.__list_directory_bare(path)

        if not entries:
            return ""

        entries = [(k, v) for k, v in entries if REGEX_MEDIA_FILE.search(k)]

        return """#EXTM3U

#EXTINF:1.0,""" + """#EXTINF:1.0,""".join((k + "\n" + v + "\n" for k, v in entries))


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def __str__(self):
        return "http://%s:%s" % threaded_server.server_address


def get_file_size(path):
    return pretty_size(os.path.getsize(path))


def get_ip_address():
    ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if ip not in (
        "127.0.0.1", "127.0.1.1", "0.0.0.0")
           ] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]

    if len(ips):
        return ips[0]
    else:
        return '0.0.0.0'

UNITS_MAPPING = [
    (1024 ** 5, ' PB'),
    (1024 ** 4, ' TB'),
    (1024 ** 3, ' GB'),
    (1024 ** 2, ' MB'),
    (1024 ** 1, ' KB'),
    (1024 ** 0, (' byte', ' bytes')),
    ]


def pretty_size(bytes, units=UNITS_MAPPING):
    """Human-readable file sizes.
    ripped from https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Local media browser with M3U playlist generator')

    parser.add_argument('webroot',
                        help='Web root directory. System root will be used if omitted',
                        nargs='?',
                        action='store',
                        default=os.path.abspath(os.sep))
    parser.add_argument('--port', '-p',
                        help='port',
                        type=int,
                        action='store',
                        default=DEFAULT_PORT)
    parser.add_argument('--domain', '-d',
                        help='domain to use in M3U playlists; by default the curren IP addres is used',
                        action='store',
                        default=get_ip_address())
    parser.add_argument('--no-browser', '-n',
                        help="don't automatically open the system web browser",
                        action='store_true',
                        default=False)
    parser.add_argument('--suppress_size', '-s',
                        help="DON'T show file size in file list",
                        action='store_true',
                        default=False)

    args = parser.parse_args(sys.argv[1:])

    print("Initializing ThreadedHTTPServer...")
    threaded_server = ThreadedHTTPServer((args.domain, args.port), MyRequestHandler)
    print("ThreadedHTTPServer init completed.")
    print(threaded_server)
    url = "http://{}:{}".format(args.domain, args.port)
    print("Serving on {}".format(url))

    if not args.no_browser and not platform.machine() in ('arm', 'aarch64', 'armv7l'):
        open_url_in_browser(url)

    threaded_server.serve_forever()
