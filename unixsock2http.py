#!/usr/bin/env python3
import os
import requests
from time import sleep
import socket
import sys


NUM_RETRIES = 10
RETRY_WAIT_S = 1


def main():
    if len(sys.argv) < 2:
        print(f"Usage: DSE_TUNNEL_PATH=socket_path {sys.argv[0]} url", file=sys.stderr)
        sys.exit(1)

    socket_path = os.environ["DSE_TUNNEL_PATH"]
    url = sys.argv[1]

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)

    print(f"Listening for incoming connections on {socket_path}...")
    conn, _ = server.accept()
    print(f"Connection received!")
    try:
        with conn.makefile("rw") as f:
            while req_text := f.readline().strip():
                for i in range(NUM_RETRIES):
                    r = requests.post(url, data=req_text)
                    if r.status_code != requests.codes.ok:
                        print(f"URL request failed with status {r.status_code}: {r.text}", file=sys.stderr)
                        sleep(RETRY_WAIT_S)
                        continue
                    print(r.text.strip(), file=f, flush=True)
                    break
                else:
                    print(f"Giving up after {i} retries", file=sys.stderr)
                    sys.exit(1)
    finally:
        conn.close()
        server.close()


if __name__ == "__main__":
    main()

