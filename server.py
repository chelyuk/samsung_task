# !/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import queue
import json

queue_list = []


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


class S(BaseHTTPRequestHandler):
    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        length = int(self.headers['Content-Length'])
        self.post_data = self.rfile.read(length)

        try:
            if self.headers['Content-Type'] == 'application/json':
                self.post_data = json.loads(self.post_data.decode("utf-8"))
                self.log_message(json.dumps(self.post_data))

                qnumber = self.post_data["qnumber"]

                if qnumber < 0 or qnumber >= len(queue_list):
                    raise Error("E: Queue number is out of range")

                if queue_list[qnumber].empty():
                    raise Error("E: Queue ia empty")

                self._set_headers(200)
                self.wfile.write(bytes(json.dumps(queue_list[qnumber].get()), "utf-8"))

        except Error as error:
            self.log_message("%s" % error)
            self._set_headers(400)
            self.wfile.write(bytes(str(error).encode("utf-8")))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        self.post_data = self.rfile.read(length)

        try:
            if self.headers['Content-Type'] == 'application/json':
                self.post_data = json.loads(self.post_data.decode("utf-8"))
                self.log_message(json.dumps(self.post_data))

                message = self.post_data["message"]
                if message is None:
                    raise Error("E: Message is empty")

                qnumber = self.post_data["qnumber"]
                if qnumber < 0 or qnumber >= len(queue_list):
                    raise Error("E: Queue number is out of range")

                queue = queue_list[qnumber]
                if queue.full():
                    raise Error("E: Queue is full")

                queue_list[qnumber].put(message)

                self._set_headers(200)

        except Error as error:
            self.log_message("%s" % error)
            self._set_headers(400)
            self.wfile.write(bytes(str(error).encode("utf-8")))


def main(args):

    for i in range(10000):
        queue_list.append(queue.Queue(maxsize=5))

    server_class = HTTPServer
    handler_class = S

    server_address = (args.host, int(args.port))
    server = server_class(server_address, handler_class)
    print('Starting server...')
    server.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Server to work with http requests.')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='ip address')
    parser.add_argument('--port', type=str, default='80', help='Port to establish connection. Default: 80')

    args = parser.parse_args()

    main(args)
