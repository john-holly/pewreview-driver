#!/usr/bin/env python3

#
# Author: John Holly
#
# Driver for Dream Cheeky USB Missile Launcher (The green/black model with 3 darts).
# Don't buy it from here, this is just the same model..
#
# https://www.amazon.com/Unknown-782-USB-Missile-Launcher/dp/B000XYR2CM/ref=sr_1_4?keywords=dream+cheeky&qid=1571775979&sr=8-4
#
# Please verify your USB missile launcher's vendor ID and product ID match what is
# listed below. This will not work for the Thunder or Storm launchers.
#
#   $ lsusb
#   ...
#   Bus 003 Device 018: ID 0a81:0701 Chesen Electronics Corp. USB Missile Launcher
#

import log

from enum import Enum

import os
import sys
import time

import hid

"""
RQ_TYPE_TO_CLASS_INTERFACE (0x21 or 100001):

This is a bitfield for specifying the recipient and type of the request.
This specifies the missile launcher as a human interface device in the
setup packet.

Recipient:      Interface
Type:           Class

(In the following table D<num> is the bit position)
D7 Data Phase Transfer Direction
  0 = Host to Device
  1 = Device to Host
D6..5 Type
  0 = Standard
  1 = Class
  2 = Vendor
  3 = Reserved
D4..0 Recipient
  0 = Device
  1 = Interface
  2 = Endpoint
  3 = Other
"""
TO_CLASS_INTERFACE = 0x21
# Request type used - we are setting the configuration of hardware state
SET_CONFIGURATION = 0x09

# Vendor/Product ID
CHESEN_ELECTRONICS_CORP = 0x0a81
USB_MISSILE_LAUNCHER = 0x0701


def usleep(millis):
    time.sleep(millis / 1000.0)


class Command(Enum):
    UP = [0x02]
    DOWN = [0x01]
    LEFT = [0x04]
    RIGHT = [0x08]
    FIRE = [0x10]
    STOP = [0x20]
    STATUS = [0x40]


class TimedCommand(dict):
    def __init__(self, cmd, millis):
        self.cmd = cmd
        self.millis = millis


class Launcher():
    logger = log.get(__name__)

    def __init__(self):
        self.dev = hid.device(CHESEN_ELECTRONICS_CORP, USB_MISSILE_LAUNCHER)

        if self.dev is None:
            raise ValueError('Launcher not found.')
        else:
            self.dev.open(CHESEN_ELECTRONICS_CORP, USB_MISSILE_LAUNCHER)

    def send(self, cmd):
        self.dev.send_feature_report(cmd)

    def up(self):
        self.logger.info(Command.UP.name)
        self.send(Command.UP)

    def down(self):
        self.logger.info(Command.DOWN.name)
        self.send(Command.DOWN)

    def left(self):
        self.logger.info(Command.LEFT.name)
        self.send(Command.LEFT)

    def right(self):
        self.logger.info(Command.RIGHT.name)
        self.send(Command.RIGHT)

    def fire(self, millis=7000):
        self.logger.info(Command.FIRE.name)
        self.send(Command.FIRE)
        usleep(millis)

    def stop(self):
        """
        Stops an ongoing command

        :return:
        """
        self.logger.info(Command.STOP.name)
        self.send(Command.STOP)

    def stream(self, stream):
        """
        Execute a chain of commands

        :param stream: A list of TimedCommand
        :return:
        """
        self.logger.debug("Received stream: {}".format([c.cmd for c in stream]))
        for command in stream:
            self.logger.info(command.cmd.name)
            self.send(command.cmd.value)
            usleep(command.millis)


def demo():
    launcher = Launcher()
    launcher.stream([
        TimedCommand(Command.UP, 1000),
        TimedCommand(Command.DOWN, 1000),
        TimedCommand(Command.LEFT, 1000),
        TimedCommand(Command.RIGHT, 1000),
        TimedCommand(Command.FIRE, 7000),
        TimedCommand(Command.FIRE, 7000),
        TimedCommand(Command.FIRE, 7000),
        TimedCommand(Command.STOP, 0),
    ])


if __name__ == '__main__':
    # TODO: Create udev rules so I can run unprivileged
    if not os.geteuid() == 0:
        sys.exit("Script must be run as root.")
    demo()
