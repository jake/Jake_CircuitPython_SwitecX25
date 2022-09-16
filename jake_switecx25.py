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
import time
import digitalio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jake/Jake_CircuitPython_SwitecX25.git"

# During zeroing we will step the motor CCW with a fixed step period of 800 microseconds
SWITECX25_RESET_STEP_MICROSEC = 0.0008


# This table defines the acceleration curve as a list of(step, delay) pairs.
# 1st value is the cumulative step count since starting from rest, 2nd value is delay in microseconds.
# 1st value in each subsequent row must be > 1st value in previous row
# The delay in the last row determines the maximum angular velocity.
SWITECX25_DEFAULT_ACCELT_TABLE = [
    [20, 0.003],     # 3000
    [50, 0.0015],    # 1500
    [100, 0.001],    # 1000
    [150,  0.0008],  # 800
    [300,  0.0006]   # 600
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
        self.pins.append(digitalio.DigitalInOut(pin1))
        self.pins.append(digitalio.DigitalInOut(pin2))
        self.pins.append(digitalio.DigitalInOut(pin3))
        self.pins.append(digitalio.DigitalInOut(pin4))
        self.pins[0].direction = digitalio.Direction.OUTPUT
        self.pins[1].direction = digitalio.Direction.OUTPUT
        self.pins[2].direction = digitalio.Direction.OUTPUT
        self.pins[3].direction = digitalio.Direction.OUTPUT

        self.state_count = len(SWITECX25_STATE_MAP)
        self.current_state = 0

        self.current_step = 0       # step we are currently at
        self.target_step = 0        # target we are moving to
        self.vel = 0                # steps travelled under acceleration
        self.dir = 0                # direction -1,0,1
        self.stopped = True         # True if stopped

        self.time0 = 0              # time when we entered this state
        self.micro_delay = 0        # microsecs until next state

        # accel table which can be modified
        self.accel_table = SWITECX25_DEFAULT_ACCELT_TABLE[:]

        # fastest vel allowed defaults to last value in table
        self.max_vel = self.accel_table[len(self.accel_table)-1][0]

    def step_up(self):
        if (self.current_step < self.steps):
            self.current_step += 1
            self.current_state = (self.current_state + 1) % self.state_count
            self._write_io()

    def step_down(self):
        if (self.current_step > 0):
            self.current_step -= 1
            self.current_state = (self.current_state + 5) % self.state_count

    def zero(self):
        self.current_step = self.steps - 1

        for _ in range(self.steps):
            self.step_down()
            time.sleep(SWITECX25_RESET_STEP_MICROSEC)

        self.current_step = 0
        self.target_step = 0
        self.vel = 0
        self.dir = 0

    def update(self):
        if not self.stopped:
            if time.monotonic() - self.time0 >= self.micro_delay:
                self._advance()

    # This will give you smoother movements, but your application will block
    def update_blocking(self):
        while not self.stopped:
            if time.monotonic() - self.time0 >= self.micro_delay:
                self._advance()

    def set_position(self, pos):
        # pos is unsigned so don't need to check for <0
        if (pos >= self.steps):
            pos = self.steps-1

        self.target_step = pos

        # reset the timer to avoid possible time overflow giving spurious deltas
        if self.stopped:
            self.stopped = False
            self.time0 = time.monotonic()
            self.micro_delay = 0

    # This function determines the speed and accel
    # characteristics of the motor.  Ultimately it
    # steps the motor once (up or down) and computes
    # the delay until the next step.  Because it gets
    # called once per step per motor, the calcuations
    # here need to be as light-weight as possible, so
    # we are avoiding floating-point arithmetic.
    #
    # To model acceleration we maintain vel, which indirectly represents
    # velocity as the number of motor steps travelled under acceleration
    # since starting.  This value is used to look up the corresponding
    # delay in accelTable.  So from a standing start, vel is incremented
    # once each step until it reaches maxVel.  Under deceleration
    # vel is decremented once each step until it reaches zero.
    def _advance(self):
        # detect stopped state and exit early
        if self.current_step == self.target_step and self.vel == 0:
            self.stopped = True
            self.dir = 0
            self.time0 = time.monotonic()
            return

        # if stopped, determine direction
        if self.vel == 0:
            self.dir = 1 if self.current_step < self.target_step else -1
            # do not set to 0 or it could go negative in case 2 below
            self.vel = 1

        if self.dir > 0:
            self.step_up()
        else:
            self.step_down()

        # determine delta, number of steps in current direction to target.
        # may be negative if we are headed away from target
        delta = (self.target_step -
                 self.current_step) if self.dir > 0 else (self.current_step - self.target_step)

        if delta > 0:
            # case 1 : moving towards target (maybe under accel or decel)
            if delta < self.vel:
                # time to declerate
                self.vel -= 1
            elif self.vel < self.max_vel:
                # accelerating
                self.vel += 1
            else:
                # at full speed - stay there
                pass
        else:
            # case 2 : at or moving away from target (slow down!)
            self.vel -= 1

        # vel now defines delay
        i = 0
        # this is why vel must not be greater than the last vel in the table.
        while self.accel_table[i][0] < self.vel:
            i += 1

        self.micro_delay = self.accel_table[i][1]
        self.time0 = time.monotonic()

    def _write_io(self):
        mask = SWITECX25_STATE_MAP[self.current_state]
        for i in range(4):
            self.pins[i].value = mask & 0x1
            mask >>= 1
