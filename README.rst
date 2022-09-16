Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/jake/Jake_CircuitPython_SwitecX25/workflows/Build%20CI/badge.svg
    :target: https://github.com/jake/Jake_CircuitPython_SwitecX25/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython port of Arduino `Switec X25 library <https://github.com/clearwater/SwitecX25>`_.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install switecx25

Or the following command to update an existing version:

.. code-block:: shell

    circup update

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
