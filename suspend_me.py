#!/usr/bin/env python3

"""
    This test of suspend is really best run from another machine.  If it's run from the 
    machine being suspended, it will suspend, but the recvfrom() will probably timeout.
"""


import unittest
import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6061

class TestPingLiveServer(unittest.TestCase):
    def test_ping_live(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.sendto(b"suspend", (SERVER_HOST, SERVER_PORT))
            try:
                data, _ = s.recvfrom(1024)
                print(data.decode())
            except socket.timeout:
                self.fail("No response received from server (timeout)")

if __name__ == "__main__":
    unittest.main()
