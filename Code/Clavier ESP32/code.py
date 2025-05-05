import busio
import board

# Keyboard setup
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation

# Keys
from kmk.keys import KC
from kmk.modules.macros import Macros, Tap, Delay
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys #for mouse integration

# Extensions
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.display import Display, TextEntry, ImageEntry

# For SSD1306
from kmk.extensions.display.ssd1306 import SSD1306

# ------------------------------ KEYBOARD SETUP ------------------------------
keyboard = KMKKeyboard()
mouse = MouseKeys(
    max_speed = 25,
    acc_interval = 25, # Delta ms to apply acceleration. lower is faster
    move_step = 1
)
encoder_handler = EncoderHandler()
tapdance = TapDance()
tapdance.tap_time = 250

# ------------------------------ keyboard  ------------------------------
keyboard.modules = [encoder_handler, tapdance, mouse]
#keyboard.modules.append(mouse)

# ------------------------------ PINS DEFINITIONS ------------------------------
# MATRIX PINS
keyboard.col_pins = (board.SCK, board.MISO, board.D10, board.MOSI)
keyboard.row_pins = (board.D9, board.D8, board.D7)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

# I2C PINS
SDA_PIN = board.A2
SCL_PIN = board.A3

# ENCODER PINS
encoder_handler.pins = ((board.D6, board.D5, board.D4, False),)

# Macros
macros = Macros()

# ------------------------------ EXTENSIONS SETUP ------------------------------
# RGB setup
rgb_ext = RGB(pixel_pin = board.A0, num_pixels=12, hue_default=100, animation_mode=AnimationModes.RAINBOW)

# OLED DISPLAY
i2c_bus = busio.I2C(SCL_PIN, SDA_PIN)
driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
    # Optional:
    device_address=0x3C,
)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=64, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=20, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=60, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)

display.entries = [
    TextEntry(text="Cegep de Sherbrooke", x=64, y=0, x_anchor="M", y_anchor="T"),
    TextEntry(text="Dpt. Technologies", x=64, y=22, x_anchor="M", y_anchor="M"),
    TextEntry(text="genie electrique", x=64, y=34, x_anchor="M", y_anchor="M"),
    TextEntry(text="-------------------", x=64, y=40, x_anchor="M"),
    TextEntry(text="Clavier de macros", x=64, y=64, x_anchor="M", y_anchor="B"),
]


media_ext = MediaKeys()
keyboard.extensions = [rgb_ext, display, media_ext, macros]

# ------------------------------ TAPDANCE  ------------------------------
TD_MEDIA = KC.TD(
    # Tap once
    KC.MEDIA_PLAY_PAUSE,
    # Tap two time
    KC.MEDIA_NEXT_TRACK,
    # Tap three time
    KC.MEDIA_PREV_TRACK,
)


# ------------------------------ MACRO  ------------------------------
NOTEPAD = KC.MACRO(Tap(KC.LWIN), Delay(50), "notepad", Delay(50), Tap(KC.ENTER))

_______ = KC.TRNS
xxxxxxx = KC.NO

# KEYMAPS
keyboard.keymap = [
    # NUMPAD
    [
        KC.MB_LMB,  KC.MS_UP, KC.W,  KC.BSPACE,
        KC.MS_LEFT,  KC.A, KC.MS_RIGHT,  KC.D,
        KC.MS_DOWN,  KC.MS_DOWN, KC.S,  KC.PMNS,
    ],
]

encoder_handler.map = [
        # LAUCHPAD
        ((KC.MS_LEFT, KC.MS_RIGHT, KC.MB_LMB),),
]

keyboard.debug_enabled = True
if __name__ == "__main__":
    keyboard.go()
