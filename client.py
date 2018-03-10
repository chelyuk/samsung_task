import http.client


def run(args):

    command = args.request
    address = args.host + ":" + args.port
    qnumber = args.qnumber

    print(address)
    conn = http.client.HTTPConnection(address)
    conn.request(command, "/", args.message)
    response = conn.getresponse()

    print("Response status = {}", response.status)
    print("Response reason = {}", response.reason)
    print("Response read   = {}", response.read())

    conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Client to send http requests.')
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=str, default='80')
    parser.add_argument('request', type=str)
    parser.add_argument('--message', type=str)
    parser.add_argument('--qnumber', type=int, default=0)

    args = parser.parse_args()

    run(args)
