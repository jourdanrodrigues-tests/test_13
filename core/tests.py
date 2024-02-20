from threading import Thread
from unittest import TestCase
from wsgiref.simple_server import make_server

import requests

from core.wsgi import application


class TestServer(TestCase):
    def test_that_server_turns_on_ok_through_wsgi(self):
        port = 8912
        server = make_server("", port, application)
        Thread(target=server.serve_forever).start()  # Start in a thread because it blocks the execution
        try:
            requests.get("http://localhost:{}/".format(port))
        except ConnectionError:
            raise AssertionError("Server is not starting")
        finally:
            server.shutdown()
