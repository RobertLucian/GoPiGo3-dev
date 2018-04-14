####################
AltGPG3 CLI Commands
####################

Use ``altgpg3 -h`` in your terminal to access the helper menu for it.

This CLI tool for the `GoPiGo3`_ board has the following functionalities:

1. ``action`` command is for controlling the robot to go in whichever direction.
2. ``check`` command is for checking the version of the fw, hw, voltages, serial numbers and so on.
3. ``firmware`` command is used for burning the firmware onto the `GoPiGo3`_ board.
4. ``shutdown-button` command is used for installing or uninstalling a service with systemd with which it allows the user to shutdown the Pi just by pressing the button power on the `GoPiGo3`_.

For all of these 4 commands, there's a different helper menu. So for ``altgpg3 action -h`` you'll be getting something different than for ``altgpg3 check -h``.

######################
CLI Commands Breakdown
######################

In the previous part, there are listed 4 major commands that can be used with this CLI tool.
For each of the previous commands there are other sub-commands that can be used. These are:

* ``action`` command + the following command:

  * ``forward`` - for moving the GoPiGo3 forward without stopping.
  * ``backward`` - for moving the GoPiGo3 backward without stopping.
  * ``left`` - for rotating the GoPiGo3 to the left without stopping.
  * ``right`` - for rotating the GoPiGo3 to the right without stopping.
  * ``stop`` - to stop the GoPiGo3 from doing anything.
  * ``rotate`` - to rotate the GoPiGo3 around (either to the left or right) for a given number of rotational degrees. Must be used with `--degrees-rotate` option.
  * ``dex-eyes-on`` - light up GoPiGo3 mascot's eyes. Does not support changing the color yet.
  * ``dex-eyes-off`` - turn off GoPiGo3 mascot's eyes.
  * ``-s``/``--speed`` option - can be set between 0 and 300 and it specifies how fast the GoPiGo3 can go. By default it's set to 300. Can be used with ``forward``,``backward``,``left``,``right`` and ``rotate`` commands.
  * ``-d``/``--distance`` option  - specifies how much the robot can go in one direction in centimeters. This can be a negative number for reverse or positive for the latter. Can be used with ``forward`` and ``backward`` commands.
  * ``-r``/``--degrees-rotate`` option - specifies how many degrees to rotate the GoPiGo3 on the spot. Number can be negative (to the left) or positive (to the right). Can only be used with the ``rotate`` command. By default it's set to 360 degrees.

* ``check`` command + the following command:

  * ``fw`` - to get the current firmware version on the `GoPiGo3`_ board.
  * ``hw`` - to get the hardware version of your `GoPiGo3`_ board.
  * ``info`` - to get the manufacturer name, board, serial number, versions and voltages.

* ``firmware`` command + the following command:

  * ``burn`` - to burn the firmware onto the `GoPiGo3`_ board.
  * ``-s``/``--sudo`` - appends the ``sudo`` command to any bash(shell)-issues commmands. For this, you must be

This is the python library for GoPiGo3, which is a robot car that can be programmed to do anything.

Please visit:

   * Our `official documentation <http://gopigo3.readthedocs.io>`_ for instructions on how to use the robot.
   * Our `github repo folder <https://github.com/DexterInd/GoPiGo3/tree/master/Software/Python>`_ for using one of our many example programs.
   * Or our `official page <https://www.dexterindustries.com/gopigo3/>`_ for more details about this robot.
