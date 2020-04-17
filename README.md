# Blue MPC Player

Control MPD player with your bluetooth speaker buttons.

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

**Configuration**  
Set the following constants in the blue-mpc-player script:

```python
DEVICE_PHYS = 'xx:xx:xx:xx:xx:xx'       # Your BT controller address - get with 'bluetoothctl list'
MPD_PORT = 6600                         # Your MPD server port
MPD_HOST = 'localhost'                  # Your MPD server host
DEFAULT_PLAYLIST = 'your_playlist'      # Name of your playlist
```

Run your MPD server:  
`mpd`

Run the blue-mpc-player script:  
`sudo ./blue_mpc_player.py`
