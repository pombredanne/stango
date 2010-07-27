import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class StangoRequestHandler(BaseHTTPRequestHandler):
    def start_response(self, code, headers=[]):
        if code == 200:
            self.send_response(200)
            for header in headers:
                keyword, value = header.split(': ')
                self.send_header(keyword, value)
            self.end_headers()
        else:
            self.send_response(code)

    def do_GET(self):
        manager = self.server.manager

        # remove the leading /
        realpath = path = self.path[1:]

        if manager.index_file and (not path or path.endswith('/')):
            realpath = os.path.join(path, manager.index_file)

        for filespec in manager.files:
            if filespec.realpath == realpath:
                self.start_response(200)
                self.wfile.write(manager.view(filespec, serving=True))
                break
        else:
            self.start_response(404)


class StangoHTTPServer(HTTPServer):
    def __init__(self, server_address, manager):
        self.manager = manager
        HTTPServer.__init__(self, server_address, StangoRequestHandler)