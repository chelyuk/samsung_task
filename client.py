# !/usr/bin/env python

import http.client
import json
import sys
import argparse


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(args):
    try:
        command = args.request
        address = args.host + ":" + args.port
        qnumber = args.qnumber
        message = args.message
        test_mode = args.test_mode

        if test_mode is True:

            if qnumber < 0 or qnumber >= 10000:
                raise Error("EC: Queue number is out of range")

            if command == "POST" and message is None:
                raise Error("EC: Message is empty")

    except Error as error:
        print("%s" % error)
        sys.exit(1)

    print(address)
    header = {'Content-type': 'application/json'}
    conn = http.client.HTTPConnection(address)

    message = {'qnumber': qnumber, 'message': message}

    conn.request(command, "/", json.dumps(message), header)
    response = conn.getresponse()

    print("Response status = {}", response.status)
    print("Response reason = {}", response.reason)
    print("Response read   = {}", response.read())

    conn.close()


def create_parser():
    parser = argparse.ArgumentParser(description='Client to send http requests.')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='ip address')
    parser.add_argument('--port', type=str, default='80', help='Port to establish connection. Default: 80')
    parser.add_argument('request', type=str, help='Type of request. POST or GET')
    parser.add_argument('--message', type=str, help='Text message to send on server')
    parser.add_argument('--qnumber', type=int, default=0,
                        help='Number of queue, supported range is from 0 to 10000.Default: 0')
    parser.add_argument('--test_mode', action='store_false', help='Remove message validation on client side')
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    main(args)
