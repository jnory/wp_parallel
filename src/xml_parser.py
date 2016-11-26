# coding: utf-8
from io import StringIO
import xml.sax.handler


class Revision(object):
    def __init__(self):
        self.id = None
        self.timestamp = None
        self.text = StringIO()


class Page(object):
    def __init__(self):
        self.title = None
        self.id = None
        self.revision = Revision()


class Handler(xml.sax.handler.ContentHandler):
    def __init__(self, callback):
        super().__init__()
        self.page = None
        self.state = None
        self.current = None
        self.callback = callback

    def startElement(self, name, attrs):
        if name == "page":
            self.page = Page()
            self.state = "page"
        elif name == "revision":
            self.state = "revision"
        self.current = name

    def endElement(self, name):
        if name == "revision":
            self.state = "page"
        elif name == "page":
            self.page.revision.text = self.page.revision.text.getvalue()
            self.callback(self.page)
        self.current = None

    def characters(self, content):
        if self.current == "title":
            self.page.title = content
        elif self.current == "id":
            content = content.strip()
            if self.state == "page":
                self.page.id = int(content)
            else:
                self.page.revision.id = int(content)
        elif self.current == "timestamp":
            self.page.revision.timestamp = content
        elif self.current == "text":
            self.page.revision.text.write(content)


def main(args):
    import bz2
    import xml.sax

    path = args.file
    file = bz2.BZ2File(path, "r")
    parser = xml.sax.make_parser()

    def callback(page):
        print(page.id, page.title, page.revision.id, page.revision.timestamp,
              page.revision.text)

    parser.setContentHandler(Handler(callback))
    parser.parse(file)


if __name__ == '__main__':
    def get_parser():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("file")
        return parser

    main(get_parser().parse_args())
