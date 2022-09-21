Introduction
============

CircuitPython port of Arduino `Switec X25 library <https://github.com/clearwater/SwitecX25>`_.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`

Usage Example
=============

.. code-block:: python

    import jake_switecx25

    STEPS = 315*3

    motor = jake_switecx25.Jake_SwitecX25(STEPS, board.IO2, board.IO3, board.IO4, board.IO5)
    motor.zero()
    motor.set_position(STEPS / 2)

    while True:
        motor.update()


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/jake/Jake_CircuitPython_SwitecX25/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
