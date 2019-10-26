#!/usr/bin/env python3

"""
This client will allow you to connect to a running server from this project and execute a sequence of commands
with timeouts.
"""

import socket
import sys
import log


class LauncherException(Exception):
    """Launcher hardware/software state error"""
    pass


logger = log.get("client")


def usage(exit_code=0):
    print("NOTE: CMD is one of [UP, DOWN, LEFT, RIGHT, FIRE, RESET]\n\n" +
          "python client.py --port 31337 CMD[,<sleep in nanoseconds/number of missiles>]")
    sys.exit(exit_code)


if __name__ == "__main__":
    if not len(sys.argv) > 3:
        usage(1)
    else:
        if not str.isdigit(sys.argv[2]):
            logger.error("Invalid port number")
            sys.exit(1)

        port = int(sys.argv[2])
        data = " ".join(sys.argv[3:])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect(("localhost", port))
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            if received == '' or received is None:
                raise LauncherException("Driver not responding, hardware in failed state or invalid command string sent.")
        finally:
            sock.close()

        print("Sent:     {}".format(data))
        print("Received: {}".format(received))
