# ev3dev-brickman-gamepad

## Overview
Listens to input from a USB NES controller and translates the button presses to
keystrokes to navigate the ev3dev brickman menu.

## Install

```bash
$ git clone https://github.com/dwalton76/ev3dev-brickman-gamepad.git
$ cd ev3dev-brickman-gamepad
$ sudo cp brickman-gamepad.py /usr/local/bin/
$ sudo cp brickman-gamepad.service /lib/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable brickman-gamepad.service
$ sudo systemctl start brickman-gamepad.service
```

The status for your brickman-gamepad service should look similar to:
```
robot@brickpi3:~/ev3dev-brickman-gamepad$ sudo systemctl status brickman-gamepad.service
● brickman-gamepad.service - Brickman Gamepad Service
   Loaded: loaded (/lib/systemd/system/brickman-gamepad.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2019-03-25 03:15:47 UTC; 6s ago
 Main PID: 2375 (python3)
   CGroup: /system.slice/brickman-gamepad.service
           └─2375 python3 /usr/local/bin/brickman-gamepad.py

Mar 25 03:15:47 brickpi3 systemd[1]: Started Brickman Gamepad Service.
robot@brickpi3:~/ev3dev-brickman-gamepad$
```
