#!/usr/bin/env python3

# 
# File:     blue_mpc_player.py
# Author:   Martin Hrabos
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#

import evdev
import pyudev
from evdev import ecodes
from mpd import MPDClient
from contextlib import contextmanager
import logging

DEVICE_PHYS = 'xx:xx:xx:xx:xx:xx'       # Your device phys addres comes here
MPD_PORT = 6600                         # Your MPD server port
MPD_HOST = 'localhost'                  # Your MPD server host
DEFAULT_PLAYLIST = 'your_playlist'      # Your playlist name for MPD


# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = False


class MPCHandler:
    def __init__(self, devpath):
        self.devpath = devpath
        self.device = evdev.InputDevice(self.devpath)
        self.client = MPDClient()     
        self.client.timeout = 10
        self.client.idletimeout = None
        self.load_playlist(DEFAULT_PLAYLIST)

    @contextmanager
    def connection(self):
        try:
            self.client.connect(MPD_HOST, MPD_PORT)
            yield
        except ConnectionRefusedError as err:
            log.error("Failed to connect to MPD server. Is MPD server running? %s", err)
        finally:
            self.client.close()
            self.client.disconnect()

    def disconnect(self):
        self.stop()

    def close(self):
        log.info("Closing device")
        self.device.close()

    def handle_input(self):
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_KEY and event.value == evdev.events.KeyEvent.key_down:
                    if event.code == ecodes.KEY_STOPCD:
                        log.info("STOP")
                        self.stop()
                    elif event.code == ecodes.KEY_PLAYCD:
                        log.info("PLAY/PAUSE")
                        self.play_toggle()
                    elif event.code == ecodes.KEY_PREVIOUSSONG:
                        log.info("PREVIOUS SONG")
                        self.prev_song()
                    elif event.code == ecodes.KEY_NEXTSONG:
                        log.info("NEXT SONG")
                        self.next_song()
        except:
            logging.info("Event loop ended.")


    def load_playlist(self, playlist):
        with self.connection():
            self.client.load(playlist)
            log.info("Loaded playlist: %s", playlist)

    def play(self):
        self.client.play()
        log.info("Playing: %s", self.client.currentsong())

    def pause(self):
        self.client.pause()

    def stop(self):
        with self.connection():
            self.client.stop()
    
    def next_song(self):
        with self.connection():
            self.client.next()
            log.info("Playing: %s", self.client.currentsong())

    def prev_song(self):
        with self.connection():
            self.client.previous()
            log.info("Playing: %s", self.client.currentsong())

    def play_toggle(self):
        with self.connection():
            result = self.client.status()
            if result['state'] == "stop" or result['state'] == "pause":
                self.play()
            elif result['state'] == "play":
                self.pause()

class UDEVMonitor:
    def __init__(self):
        self.mpchandler = None
        self.context = pyudev.Context()

    def run_if_device_connected(self):
        for device in self.context.list_devices(subsystem='input'):
            devname = self.get_device_devname(device)
            if devname:
                log.info("Found connected device %s at %s", DEVICE_PHYS, device.properties['DEVNAME'])
                self.mpchandler = MPCHandler(devname)
                self.mpchandler.handle_input()


    def get_device_devname(self, device):
        if 'LIBINPUT_DEVICE_GROUP' in device.properties and 'DEVNAME' in device.properties:
            if device.properties['LIBINPUT_DEVICE_GROUP'].endswith(DEVICE_PHYS) and device.properties['DEVNAME'].startswith("/dev/input/event"):
                return device.properties['DEVNAME']
        return None

    def device_action(self, device):
        if device.action == 'add':
            devname = self.get_device_devname(device)
            if devname:
                log.info("Device %s connected at %s.", DEVICE_PHYS, devname)
                self.mpchandler = MPCHandler(devname)
                self.mpchandler.handle_input()
        elif device.action == 'remove':
            devname = self.get_device_devname(device)
            if devname:
                log.info("Device %s at %s disconnected.", DEVICE_PHYS, devname)
                if self.mpchandler:
                    self.mpchandler.disconnect()
                    self.mpchandler.close()

    
    def monitor_devices(self):
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem='input')
        monitor.start()
        # Wait for input events
        for udev in iter(monitor.poll, None):
            self.device_action(udev)


if __name__ == '__main__':
    udevmonitor = UDEVMonitor()
    # Check if device already connected
    udevmonitor.run_if_device_connected()
    # Start monitoring udev
    udevmonitor.monitor_devices()

    












