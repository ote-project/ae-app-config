#!/usr/bin/env python3
import os
import socket
import sys
import requests


def main():
    if len(sys.argv) < 2:
        print(f"Usage: DSE_TUNNEL_PATH=socket_path {sys.argv[0]} url", file=sys.stderr)
        sys.exit(1)

    socket_path = os.environ["DSE_TUNNEL_PATH"]
    url = sys.argv[1]

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    server.listen(1)

    print("Listening for incoming connections...")
    conn, _ = server.accept()
    print(f"Connection received!")
    try:
        with conn.makefile("rw") as f:
            while req_text := f.readline().strip():
                r = requests.post(url, data=req_text)
                if r.status_code != requests.codes.ok:
                    print(f"URL request failed with status {r.status_code}: {r.text}", file=sys.stderr)
                    sys.exit(1)
                print(r.text.strip(), file=f, flush=True)
    finally:
        conn.close()
        server.close()


if __name__ == "__main__":
    main()

