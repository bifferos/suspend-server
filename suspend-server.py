#!/usr/bin/env python3

"""
A simple UDP server that listens for command to suspend the system or respond to ping requests.
"""

import socket
import subprocess
from pathlib import Path
import configparser
import dbus
import json
import time
from argparse import ArgumentParser



BUFFER_SIZE = 1024


def wait_for_network(timeout=30):
    """Wait until NetworkManager reports the network is connected."""
    bus = dbus.SystemBus()
    proxy = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
    iface = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    start = time.time()
    while True:
        state = iface.Get('org.freedesktop.NetworkManager', 'State')
        # 70 = NM_STATE_CONNECTED_GLOBAL
        if state == 70:
            return True
        if time.time() - start > timeout:
            return False
        time.sleep(0.5)


def suspend():
    """Suspend the system."""
    result = subprocess.run(['systemctl', 'suspend', '-i'])
    wait_for_network()
    return repr(result.returncode)


def ping():
    return "pong"


AVAILABLE_COMMANDS = {
    'suspend': suspend,
    "ping": ping
}


def run_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"UDP server listening on {host}:{port}")
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            command = data.decode().strip()
            print(f"Received command: {command} from {addr}")
            try:
                if command in AVAILABLE_COMMANDS:
                    result = AVAILABLE_COMMANDS[command]()
                else:
                    result = "Command not found"
            except Exception as e:
                result = f"Error executing command {e}"
            s.sendto(result.encode(), addr)


def main():
    parser = ArgumentParser()
    parser.add_argument('--config', type=str, default="/etc/suspend-server/config.json", help='Config file')

    args = parser.parse_args()

    if args.config:
        config = json.load(Path(args.config).open())
    else:
        config = {}

    host = config.get('listen_host', "0.0.0.0")
    port = config.get('listen_port', 6061)

    run_server(host, port)


if __name__ == "__main__":
    main()