#!/usr/bin/env python
# encoding: utf-8

import serial
import time
import sys

class Conffer(object):
    def __init__(self, serialport, filename):
        self.serial = serial.Serial(serialport, 9600, timeout=1)
        self.file = open(filename, 'r')
        self.write()

    def write_line(self, line):
        sys.stdout.write(line)
        for x in line:
            self.serial.write(x.encode("utf-8"))
            time.sleep(0.1)
        self.wait_newline()

    def wait_newline(self):
        tobreak = False
        while True:
            m = self.serial.read()
            if not m:
                if tobreak:
                    break
                time.sleep(0.1)
                continue
            sys.stdout.write(m.decode("utf-8"))
            if ord(m) in [10, 13]:
                tobreak = True

    def write(self):
        for line in self.file.readlines():
            if line.strip().startswith("#") or line.strip().startswith("!") or not line.strip():
                continue
            if not line.endswith('\n'):
                line = "%s\n" % line
            self.write_line(line)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage %s serial file" % sys.argv[0])
        sys.exit(1)
    Conffer(sys.argv[1], sys.argv[2])
