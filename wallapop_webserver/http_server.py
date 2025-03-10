import os
import webbrowser
from flask import Flask, send_from_directory
from werkzeug.serving import make_server
from utils import get_local_ip

class HTTPServer:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.app = Flask(__name__, static_folder=None) 
        self.server = None

        self.app.add_url_rule('/', 'index', self.serve_html)
        self.app.add_url_rule('/<path:path>', 'static', self.serve_static)

    def serve_html(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        webclient_dir = os.path.join(project_root, 'wallapop_webclient/dist')
        return send_from_directory(webclient_dir, 'index.html')

    def serve_static(self, path):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        webclient_dir = os.path.join(project_root, 'wallapop_webclient/dist')
        return send_from_directory(webclient_dir, path)

    def stop(self):
        if self.server:
            self.server.shutdown()

    def run(self):
        webbrowser.open(f"http://{get_local_ip()}:8080")

        self.server = make_server(self.host, self.port, self.app)
        self.server.serve_forever()
