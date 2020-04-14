# Blue MPC Player

Control MPC player with your bluetooth speaker buttons.

## Installation

`git clone https://github.com/Microtus62/blue-mpc-player.git`
`cd blue-mpc-player`

### Needed software installed

**Required:**
MPD - Music Player Daemon (server)
Pulseaudio with pulseaudio-bluetooth or bluez-alsa

**Optional:**
MPC - Command line utility for controlling MPD (client)
Cantata - Frontent for MPD (client)

### Dependencies

`python3`
`python-udev (pyudev)`
`python-evdev`
`python-mpd2`

## Usage

Run your MPD server:
`mpd`

Run the blue-mpc-player script:
`sudo ./blue_mpc_player.py`
