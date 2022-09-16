# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jacob Bijani for The Bijani Company
#
# SPDX-License-Identifier: MIT
"""
`jake_switecx25`
================================================================================

Port of Arduino SwitecX25 library


* Author(s): Jacob Bijani

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
import digitalio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jake/Jake_CircuitPython_SwitecX25.git"

# During zeroing we will step the motor CCW
# with a fixed step period defined by RESET_STEP_MICROSEC
SWITECX25_RESET_STEP_MICROSEC = 800

# This table defines the acceleration curve as a list of(step, delay) pairs.
# 1st value is the cumulative step count since starting from rest, 2nd value is delay in microseconds.
# 1st value in each subsequent row must be > 1st value in previous row
# The delay in the last row determines the maximum angular velocity.
SWITECX25_DEFAULT_ACCELT_TABLE = [
    [20, 3000],
    [50, 1500],
    [100, 1000],
    [150,  800],
    [300,  600]
]


# experimentation suggests that 400uS is about the step limit
# with my hand-made needles made by cutting up aluminium from
# floppy disk sliders.  A lighter needle will go faster.

# State  3 2 1 0   Value
# 0      1 0 0 1   0x9
# 1      0 0 0 1   0x1
# 2      0 1 1 1   0x7
# 3      0 1 1 0   0x6
# 4      1 1 1 0   0xE
# 5      1 0 0 0   0x8
SWITECX25_STATE_MAP = [0x9, 0x1, 0x7, 0x6, 0xE, 0x8]


class Jake_SwitecX25:
    def __init__(self, steps, pin1, pin2, pin3, pin4):
        self.steps = steps

        self.pins = []
        self.pins[0] = digitalio.DigitalInOut(pin1)
        self.pins[0].direction = digitalio.Direction.OUTPUT
        self.pins[1] = digitalio.DigitalInOut(pin2)
        self.pins[1].direction = digitalio.Direction.OUTPUT
        self.pins[2] = digitalio.DigitalInOut(pin3)
        self.pins[2].direction = digitalio.Direction.OUTPUT
        self.pins[3] = digitalio.DigitalInOut(pin4)
        self.pins[3].direction = digitalio.Direction.OUTPUT

        self.state_count = len(SWITECX25_STATE_MAP)
        self.current_state = 0

        self.current_step = 0       # step we are currently at
        self.target_step = 0        # target we are moving to
        self.vel = 0                # steps travelled under acceleration
        self.dir = 0                # direction -1,0,1
        self.stopped = True         # True if stopped

        self.time0                  # time when we entered this state
        self.micro_delay            # microsecs until next state

        # accel table which can be modified
        self.accel_table = SWITECX25_DEFAULT_ACCELT_TABLE[:]

        # fastest vel allowed defaults to last value in table
        self.max_vel = self.accel_table[len(self.accel_table)-1][0]

    def step_up(self):
        pass

    def step_down(self):
        pass

    def zero(self):
        pass

    def update(self):
        return 0

    def update_blocking(self):
        pass

    def set_position(self, pos):
        pass

    def _advance(self):
        pass

    def _write_io(self):
        pass
