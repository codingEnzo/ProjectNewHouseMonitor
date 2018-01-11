# -*- coding: utf-8 -*-
# webhook.py
import json
import os
from http.server import BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        raw_post_data = self.rfile.read(content_length)
        post_data = json.loads(raw_post_data.decode())
        if post_data.get('ref'):
            # 提取 branch 名字
            branch = post_data.get('ref').split('/')[-1]
            if branch == 'dev_airflow':
                os.system('fab -R worker update')
                print('Done.')
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))
