import argparse
import subprocess
import shlex

#############################################################
parser = argparse.ArgumentParser(description='This is a command-line tool for interfacing with the GoPiGo3 board\n'\
                                 'It can be used for:\n'\
                                 '1. Remotely controlling a GoPiGo3 robot.\n'\
                                 '2. Installing/Uninstalling the shutdown button service.\n'\
                                 '3. Checking the fw/hw and retrieving more info about it.\n'\
                                 '4. Flashing the fw.',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', '--version', action='store_true', required=False, help='Retrieve the version of the AltGPG3 pip package.')
#############################################################

#############################################################
subparsers = parser.add_subparsers(help='sub-command help')

go_parser = subparsers.add_parser('action', description='Sub-commands for controlling the GoPiGo3.')
check_parser = subparsers.add_parser('check', description='Sub-commands for checking the GoPiGo3.')
fw_parser = subparsers.add_parser('firmware', description='Firmware related stuff of the GoPiGo3.')
shutdown_button_parser = subparsers.add_parser('shutdown-button', description='Sub-commands for installing/uninstalling the shutdown button support.')
#############################################################

#############################################################
go_parser_actions = (
    'forward',
    'backward',
    'left',
    'right',
    'stop',
    'rotate',
    'dex-eyes-on',
    'dex-eyes-off'
)
go_parser.add_argument(action='store', choices=go_parser_actions, dest='action_command', help='Commands used for controlling the GoPiGo3 robot.')
go_parser.add_argument('-b', '--blocking', action='store_true', help='Set commands to be in blocking mode. By default, the commands are in non-blocking mode. Can be used for {forward, backward, rotate} commands.')
go_parser.add_argument('-s', '--speed', action='store', type=int, default=300, help='Speed of the motors (from 0 -> 300). By default, the speed is set to 300. Can be used for {forward, backward, left, right, rotate} commands.')
go_parser.add_argument('-d', '--distance', action='store', type=int, default=0, help='How much distance in centimeters the robot has to move. The number can be either positive or negative. Can be used for {forward, backward} commands.')
go_parser.add_argument('-r', '--degrees-rotate', action='store', type=int, default=360, help='Specifies the robot how many degrees to rotate on the spot. One full rotation is equivalent to 360 degrees. ' + \
                                                                                'The number can be either positive or negative and must be an integer. When the option is not specified, the number is set to 360. Can be used for {rotate} command.')

check_parser_actions = (
    'fw',
    'hw',
    'info'
)
check_parser.add_argument(action='store', choices=check_parser_actions, dest='action_check', help='Commands for detecting/checking the GoPiGo3 board.')

fw_parser_actions = (
    'burn',
)
fw_parser.add_argument(action='store', choices=fw_parser_actions, dest='action_firmware', help='Command for burning the firmware on the GoPiGo3.')
fw_parser.add_argument('-s', '--sudo', action='store_true', help='Appends the sudo command to whatever command is run. This is required if only the fw-burning tools are not installed and if they require higher privileges.')

shutdown_button_parser_actions = (
    'configure',
    'uninstall'
)
shutdown_button_parser.add_argument(action='store', choices=shutdown_button_parser_actions, dest='action_shutdown_button', help='Commands for configuring/uninstalling the shutdown button of the GoPiGo3. \
Having it installed, allows the user to shutdown the Pi, by pressing on the button found on the GoPiGo3.')
#############################################################

def run_command(command, cwd = None, get_output_instead = False, console_out = True):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, cwd = cwd, close_fds=True, bufsize=1)

    output_instead = ""
    for line in iter(process.stdout.readline, b''):
        line_output = line.decode('utf-8')
        if console_out:
            print(line_output.strip('\n'))
        if get_output_instead:
            output_instead += line_output

    process.stdout.close()
    process.wait()
    rc = process.poll()

    if get_output_instead:
        return output_instead
    else:
        return rc

def main():
    # parsing command line arguments
    args = parser.parse_args()
    dict_args = vars(args)

    # the default name given to the following variable
    # must be the same as the name given in the setup.py
    # and it also must be an unique identifier in this file
    insert_pkgname_here = 'travis_package_name'

    if args.version:
        import pkg_resources as pkg
        print(insert_pkgname_here + ": " + pkg.get_distribution(insert_pkgname_here).version)
    else:

        import spidev
        test_spidev = spidev.SpiDev()
        try:
            test_spidev.open(0, 1)
        except Exception:
            print("SPI is not enabled.")
            return 1

        if 'action_command' in dict_args:
            from altgpg3 import easygopigo3 as easy

            # entered action subparser
            # this parser deals with controlling the GoPiGo3 (physically)

            try:
                robot = easy.EasyGoPiGo3()
            except IOError:
                print("The GoPiGo3 board does not appear to be connected - command not issued.")
                robot = None
            except easy.gopigo3.FirmwareVersionError as fw_error:
                print(str(fw_error))
                robot = None
            except Exception as error:
                print(str(error))
                robot = None

            if robot is not None:
                blocking = args.blocking
                speed = args.speed
                distance = args.distance
                degrees_rotate = args.degrees_rotate

                if args.action_command == 'forward':
                    robot.set_speed(speed)
                    if blocking is True:
                        robot.drive_cm(distance, blocking)
                    else:
                        if distance > 0:
                            robot.drive_cm(distance, blocking)
                        else:
                            robot.forward()
                elif args.action_command == 'backward':
                    if blocking is True:
                        robot.drive_cm(-distance, blocking)
                    else:
                        if distance > 0:
                            robot.drive_cm(-distance, blocking)
                        else:
                            robot.backward()
                elif args.action_command == 'right':
                    robot.set_speed(speed)
                    robot.right()
                elif args.action_command == 'left':
                    robot.set_speed(speed)
                    robot.left()
                elif args.action_command == 'stop':
                    robot.set_speed(speed)
                    robot.stop()
                elif args.action_command == 'rotate':
                    robot.set_speed(speed)
                    robot.turn_degrees(degrees_rotate, blocking)
                elif args.action_command == 'dex-eyes-on':
                    robot.open_eyes()
                elif args.action_command == 'dex-eyes-off':
                    robot.close_eyes()
                else:
                    return 2

        elif 'action_check' in dict_args:
            from altgpg3 import gopigo3
            try:
                gpg3 = gopigo3.GoPiGo3()

                if args.action_check == 'fw':
                    print("v" + gpg3.get_version_firmware())
                elif args.action_check == 'hw':
                    print('v' + gpg3.get_version_hardware())
                elif args.action_check == 'info':
                    print("Manufacturer    : ", gpg3.get_manufacturer())  # read and display the serial number
                    print("Board           : ", gpg3.get_board())  # read and display the serial number
                    print("Serial Number   : ", gpg3.get_id())  # read and display the serial number
                    print("Hardware version: ", gpg3.get_version_hardware())  # read and display the hardware version
                    print("Firmware version: ", gpg3.get_version_firmware())  # read and display the firmware version
                    print("Battery voltage : ", gpg3.get_voltage_battery())  # read and display the current battery voltage
                    print("5v voltage      : ", gpg3.get_voltage_5v())  # read and display the current 5v regulator voltage

            except OSError as error_msg:
                print(str(error_msg))
                return 3

            except gopigo3.FirmwareVersionError as error_msg:
                print(str(error_msg))
                return 3

            except Exception as unknown_error:
                print(str(unknown_error))
                return 3

        elif 'action_firmware' in dict_args:
            if args.action_firmware == 'burn':
                import pkg_resources as pkg
                updater_path = pkg.resource_filename(insert_pkgname_here, 'additional-files/firmware_burner.sh')
                updater_dir = pkg.resource_filename(insert_pkgname_here, 'additional-files')

                if args.sudo:
                    status = run_command('sudo bash ' + updater_path, cwd=updater_dir)
                else:
                    status = run_command('bash ' + updater_path, cwd=updater_dir)

                print('============================================')
                if status == 0:
                    print('The firmware has been bit-banged successfully on the SPI lines.')
                else:
                    print('The firmware couldn\'t be flashed on the GoPiGo3 board.')

        elif 'action_shutdown_button' in dict_args:
            if args.action_shutdown_button == 'configure':
                import pkg_resources as pkg

                if '0 loaded' in run_command('systemctl list-units --type=service | grep gpg3_power.service', get_output_instead=True, console_out=False):
                    # this means nothing is installed yet

                    additional_files_path = pkg.resource_filename(insert_pkgname_here, 'additional-files')
                    runnable_path = additional_files_path + '/gpg3_power.py'
                    service_path = additional_files_path + '/gpg3_power.service'

                    run_command('sudo mkdir gopigo3', cwd='/opt/', console_out = False)
                    run_command('sudo cp ' + runnable_path + ' /opt/gopigo3/', console_out = False)
                    run_command('sudo cp ' + service_path + ' /lib/systemd/system/', console_out = False)
                    run_command('sudo systemctl daemon-reload', console_out = False)

                    run_command('sudo systemctl enable gpg3_power.service', console_out = False)
                    run_command('sudo systemctl start gpg3_power.service', console_out = False)

                else:
                    # this means the service is installed but not activated/enabled
                    run_command('sudo systemctl enable gpg3_power.service', console_out = False)
                    run_command('sudo systemctl start gpg3_power.service', console_out = False)
                    run_command('sudo systemctl start gpg3_power.service', console_out = False)

            elif args.action_shutdown_button == 'uninstall':

                run_command('sudo systemctl -q stop gpg3_power.service', console_out = False)
                run_command('sudo systemctl -q disable gpg3_power.service', console_out = False)
                run_command('sudo rm -f /lib/systemd/system/gpg3_power.service', console_out = False)
                run_command('sudo systemctl daemon-reload', console_out = False)

                run_command('sudo rm -rf /opt/gopigo3', console_out = False)

        else:
            import pkg_resources as pkg
            from rst2ansi import rst2ansi
            readme_path = pkg.resource_filename(insert_pkgname_here, 'additional-files/README.rst')

            print('Enter "' + insert_pkgname_here + ' -h" or "' + insert_pkgname_here ' --help" for instructions on how to use the command line to interface with the GoPiGo3\n')
            with open(readme_path, 'r') as f:
                print(rst2ansi(f.read().encode('utf-8')))
