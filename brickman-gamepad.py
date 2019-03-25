#!/usr/bin/env python3

"""
Listens to input from a USB NES controller and translates the button presses to
keystrokes to navigate the ev3dev brickman menu.
"""

from evdev import InputDevice, ecodes, UInput
from pprint import pformat
import logging

js_map = {
    0x08: ecodes.KEY_BACKSPACE,  # BACKSPACE
    0x09: ecodes.KEY_TAB,        # TAB
    0x0D: ecodes.KEY_ENTER,      # ENTER
    0x10: ecodes.KEY_LEFTSHIFT,  # SHIFT
    0x11: ecodes.KEY_LEFTCTRL,   # CTRL
    0x12: ecodes.KEY_LEFTALT,    # ALT
    0x13: ecodes.KEY_PAUSE,      # PAUSE
    0x14: ecodes.KEY_CAPSLOCK,   # CAPS_LOCK
    0x1B: ecodes.KEY_ESC,        # ESC
    0x20: ecodes.KEY_SPACE,      # SPACE
    0x21: ecodes.KEY_PAGEUP,     # PAGE_UP # also NUM_NORTH_EAST
    0x22: ecodes.KEY_DOWN,       # PAGE_DOWN # also NUM_SOUTH_EAST
    0x23: ecodes.KEY_END,        # END # also NUM_SOUTH_WEST
    0x24: ecodes.KEY_HOME,       # HOME # also NUM_NORTH_WEST
    0x25: ecodes.KEY_LEFT,       # LEFT # also NUM_WEST
    0x26: ecodes.KEY_UP,         # UP # also NUM_NORTH
    0x27: ecodes.KEY_RIGHT,      # RIGHT # also NUM_EAST
    0x28: ecodes.KEY_DOWN,       # DOWN # also NUM_SOUTH
    0x2D: ecodes.KEY_INSERT,     # INSERT # also NUM_INSERT
    0x2E: ecodes.KEY_DELETE,     # DELETE # also NUM_DELETE
    0x30: ecodes.KEY_0,          # ZERO
    0x31: ecodes.KEY_1,          # ONE
    0x32: ecodes.KEY_2,          # TWO
    0x33: ecodes.KEY_3,          # THREE
    0x34: ecodes.KEY_4,          # FOUR
    0x35: ecodes.KEY_5,          # FIVE
    0x36: ecodes.KEY_6,          # SIX
    0x37: ecodes.KEY_7,          # SEVEN
    0x38: ecodes.KEY_8,          # EIGHT
    0x39: ecodes.KEY_9,          # NINE
    0x41: ecodes.KEY_A,          # A
    0x42: ecodes.KEY_B,          # B
    0x43: ecodes.KEY_C,          # C
    0x44: ecodes.KEY_D,          # D
    0x45: ecodes.KEY_E,          # E
    0x46: ecodes.KEY_F,          # F
    0x47: ecodes.KEY_G,          # G
    0x48: ecodes.KEY_H,          # H
    0x49: ecodes.KEY_I,          # I
    0x4A: ecodes.KEY_J,          # J
    0x4B: ecodes.KEY_K,          # K
    0x4C: ecodes.KEY_L,          # L
    0x4D: ecodes.KEY_M,          # M
    0x4E: ecodes.KEY_N,          # N
    0x4F: ecodes.KEY_O,          # O
    0x50: ecodes.KEY_P,          # P
    0x51: ecodes.KEY_Q,          # Q
    0x52: ecodes.KEY_R,          # R
    0x53: ecodes.KEY_S,          # S
    0x54: ecodes.KEY_T,          # T
    0x55: ecodes.KEY_U,          # U
    0x56: ecodes.KEY_V,          # V
    0x57: ecodes.KEY_W,          # W
    0x58: ecodes.KEY_X,          # X
    0x59: ecodes.KEY_Y,          # Y
    0x5A: ecodes.KEY_Z,          # Z
    0x5B: ecodes.KEY_LEFTMETA,   # META # WIN_KEY_LEFT
    0x5C: ecodes.KEY_RIGHTMETA,  # WIN_KEY_RIGHT
    0x60: ecodes.KEY_KP0,        # NUM_ZERO
    0x61: ecodes.KEY_KP1,        # NUM_ONE
    0x62: ecodes.KEY_KP2,        # NUM_TWO
    0x63: ecodes.KEY_KP3,        # NUM_THREE
    0x64: ecodes.KEY_KP4,        # NUM_FOUR
    0x65: ecodes.KEY_KP5,        # NUM_FIVE
    0x66: ecodes.KEY_KP6,        # NUM_SIX
    0x67: ecodes.KEY_KP7,        # NUM_SEVEN
    0x68: ecodes.KEY_KP8,        # NUM_EIGHT
    0x69: ecodes.KEY_KP9,        # NUM_NINE
    0x6A: ecodes.KEY_KPASTERISK, # NUM_MULTIPLY
    0x6B: ecodes.KEY_KPPLUS,     # NUM_PLUS
    0x6D: ecodes.KEY_KPMINUS,    # NUM_MINUS
    0x6E: ecodes.KEY_KPDOT,      # NUM_PERIOD
    0x6F: ecodes.KEY_KPSLASH,    # NUM_DIVISION
    0x70: ecodes.KEY_F1,         # F1
    0x71: ecodes.KEY_F2,         # F2
    0x72: ecodes.KEY_F3,         # F3
    0x73: ecodes.KEY_F4,         # F4
    0x74: ecodes.KEY_F5,         # F5
    0x75: ecodes.KEY_F6,         # F6
    0x76: ecodes.KEY_F7,         # F7
    0x77: ecodes.KEY_F8,         # F8
    0x78: ecodes.KEY_F9,         # F9
    0x79: ecodes.KEY_F10,        # F10
    0x7A: ecodes.KEY_F11,        # F11
    0x7B: ecodes.KEY_F12,        # F12
    0x90: ecodes.KEY_NUMLOCK,    # NUMLOCK
    0x91: ecodes.KEY_SCROLLLOCK, # SCROLL_LOCK
    0xBA: ecodes.KEY_SEMICOLON,  # SEMICOLON
    0xBC: ecodes.KEY_COMMA,      # COMMA
    0xBE: ecodes.KEY_DOT,        # PERIOD
    0xBF: ecodes.KEY_SLASH,      # SLASH
    0xC0: ecodes.KEY_GRAVE,      # APOSTROPHE
    0xDE: ecodes.KEY_APOSTROPHE, # SINGLE_QUOTE
    0xDB: ecodes.KEY_LEFTBRACE,  # OPEN_SQUARE_BRACKET
    0xDC: ecodes.KEY_BACKSLASH,  # BACKSLASH
    0xDD: ecodes.KEY_RIGHTBRACE, # CLOSE_SQUARE_BRACKET
}


class Keyboard:

    def __init__(self):
        self.uinput = UInput()

    def close(self):
        self.uinput.close()

    def send_key(self, js_keycode, state):
        self.uinput.write(ecodes.EV_KEY, js_map[js_keycode], 1 if state else 0)
        self.uinput.syn()


# Map keyboard button names to their keyboard ID
keystroke_ids = {
    'UP'    : 38,
    'DOWN'  : 40,
    'LEFT'  : 37,
    'RIGHT' : 39,
    'ENTER' : 13,
    'BACK'  : 8,
}


class DpadController(object):
    """
    Base class for NES and SNES USB controllers
    """

    BUTTON_NAME_TO_KEYSTROKE_NAME = {
        "start" : "ENTER",
        "select" : None,
        "Y" : "BACK",
        "X" : "ENTER",
        "B" : "BACK",
        "A" : "ENTER",
        "UP" : "UP",
        "DOWN" : "DOWN",
        "LEFT" : "LEFT",
        "RIGHT" : "RIGHT",
    }

    def __init__(self):

        # creates object 'device' to store the data
        self.device = InputDevice('/dev/input/event0')

        # prints device info at start
        log.info(self.device)
        log.info("\n" + pformat(self.device.capabilities(verbose=True)))

    def main(self):
        keyboard = Keyboard()
        dpad_up_down = None
        dpad_left_right = None

        # evdev takes care of polling the controller in a loop
        for event in self.device.read_loop():
            keystroke = None
            #log.debug("type %s, value %s, code %s" % (event.type, event.value, event.code))

            if event.type == ecodes.EV_KEY:
                nes_button = self.gamepad_code_to_button_name.get(event.code)
                assert nes_button, "Invalid BUTTON: type %s, value %s, code %s" % (event.type, event.value, event.code)
                pressed = bool(event.value)
                keystroke = self.BUTTON_NAME_TO_KEYSTROKE_NAME.get(nes_button)
                log.info("BUTTON %s %s -> %s" % (nes_button, "pressed" if pressed else "released", keystroke))

            elif event.type == ecodes.EV_ABS:
                value = event.value
                code = event.code
                pressed = None

                if value == 0 and code == 1:
                    dpad_up_down = "UP"
                    dpad_button = "UP"
                    pressed = True

                elif value == 255 and code == 1:
                    dpad_up_down = "DOWN"
                    dpad_button = "DOWN"
                    pressed = True

                elif value == 0 and code == 0:
                    dpad_left_right = "LEFT"
                    dpad_button = "LEFT"
                    pressed = True

                elif value == 255 and code == 0:
                    dpad_left_right = "RIGHT"
                    dpad_button = "RIGHT"
                    pressed = True

                # release event for UP or DOWN
                elif value in (127, 128) and code == 1:

                    if dpad_up_down == "UP":
                        dpad_up_down = "UP"
                        dpad_button = "UP"
                        pressed = False
                    elif dpad_up_down == "DOWN":
                        dpad_up_down = "DOWN"
                        dpad_button = "DOWN"
                        pressed = False
                    else:
                        log.warning("D-PAD: dpad_up_down %s, type %s, value %s, code %s" %
                            (dpad_up_down, event.type, event.value, event.code))
                        dpad_up_down = None
                        dpad_button = None

                # release event for LEFT or RIGHT
                elif value in (127, 128) and code == 0:

                    if dpad_left_right == "LEFT":
                        dpad_left_right = "LEFT"
                        dpad_button = "LEFT"
                        pressed = False
                    elif dpad_left_right == "RIGHT":
                        dpad_left_right = "RIGHT"
                        dpad_button = "RIGHT"
                        pressed = False
                    else:
                        log.warning("D-PAD: dpad_left_right %s, type %s, value %s, code %s" %
                            (dpad_left_right, event.type, event.value, event.code))
                        dpad_left_right = None
                        dpad_button = None

                else:
                    raise Exception("Invalid D-PAD: type %s, value %s, code %s" % (event.type, event.value, event.code))

                #log.debug("D-PAD: type %s, value %s, code %s, %s" % (event.type, event.value, event.code, button))
                keystroke = self.BUTTON_NAME_TO_KEYSTROKE_NAME.get(dpad_button)
                log.info("D-PAD %s %s -> %s" % (dpad_button, "pressed" if pressed else "released", keystroke))

            if keystroke:
                keystroke_id = keystroke_ids.get(keystroke)

                if keystroke_id:
                    keyboard.send_key(keystroke_id, pressed)


class NESController(DpadController):

    # device /dev/input/event0, name "2Axes 11Keys Game  Pad", phys "usb-3f980000.usb-1.2/input0"
    gamepad_code_to_button_name = {
        312: 'select',
        313: 'start',
        305: 'B',
        304: 'A',
    }


class SNESController(DpadController):
    """
    I own two SNES controllers but none of their codes overlap so for now will use
    the same class for both of them for now.
    """

    gamepad_code_to_button_name = {

        # TOMEE USB Controller
        # Item M05176 / 3625PO8
        # device /dev/input/event0, name "2Axes 11Keys Game  Pad", phys "usb-3f980000.usb-1.2/input0"
        312 : 'select',
        313 : 'start',
        306 : 'B',
        305 : 'A',
        307 : 'Y',
        304 : 'X',
        308 : 'left-trigger',
        309 : 'right-trigger',

        # iBUFFALO Classic USB Gamepad
        # BSGP801
        # S/N A50201
        # device /dev/input/event0, name "USB,2-axis 8-button gamepad  ", phys "usb-3f980000.usb-1.2/input0"
        294 : 'select',
        295 : 'start',
        289 : 'B',
        288 : 'A',
        291 : 'Y',
        290 : 'X',
        292 : 'left-trigger',
        293 : 'right-trigger',
    }



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        #filename="/var/log/brickman-gamepad.log",
                        format='%(asctime)s %(filename)20s %(levelname)8s: %(message)s')
    log = logging.getLogger(__name__)

    # Color the errors and warnings in red
    logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))

    gamepad = NESController()
    #gamepad = SNESController()
    gamepad.main()
