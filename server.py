from launcher import Launcher, TimedCommand, Command
import log

import sys

import socketserver

logger = log.get("server")
launcher = Launcher()

def usage(exit_code=0):
    print("python server.py [--port 31337]")
    sys.exit(exit_code)


class LaunchControl(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        decoded = self.data.decode('utf-8')
        logger.info("{} wrote: {}".format(self.client_address[0], decoded))
        commands = decoded.split()

        timed_cmds = list()
        for cmd_str in commands:
            if "," in cmd_str:
                cmd, timeout = cmd_str.split(",")
                timed_cmds.append(TimedCommand(Command[cmd], int(timeout)))
            else:
                timed_cmds.append(TimedCommand(Command[cmd_str], 0))
        # Append an extra STOP in case of omission
        timed_cmds.append(TimedCommand(Command.STOP, 0))
        print(timed_cmds)
        launcher.chain(timed_cmds)

        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage(1)
    else:
        if not str.isdigit(sys.argv[2]):
            logger.error("Invalid port number")
            sys.exit(1)

        port = int(sys.argv[2])
        server = socketserver.TCPServer(("localhost", port), LaunchControl)
        server.serve_forever()
