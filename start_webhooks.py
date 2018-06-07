#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import HTTPServer
from webhooks import S

serv = HTTPServer(("", 8001), S)
serv.serve_forever()
