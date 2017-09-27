import argparse

#############################################################
parser = argparse.ArgumentParser(description='This is a command-line tool for interfacing with the GoPiGo3 board\n'\
                                 'It can be used for:\n'\
                                 '1. Remotely controlling a GoPiGo3 robot.\n'\
                                 '2. Installing/Uninstalling the shutdown button support.\n'\
                                 '3. Checking the firmware and retrieving more info about it.\n'\
                                 '4. Flashing the firmware.',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', '--version', action='store_true', required=False, help='Retrieve the version of the GoPiGo3-dev pip package.')
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
go_parser.add_argument('-r', '--degrees-rotate', action='store', type=int, default=360, help='Specifies the robot how many degrees it has to rotate on the spot. One full rotation is equivalent to 360 degrees. ' + \
                                                                                'The number can be either positive or negative and must be an integer. When the option is not specified, the number is set to 360. Can be used for {rotate} command.')

check_parser_actions = (
    'firmware',
    'info'
)
check_parser.add_argument(action='store', choices=check_parser_actions, dest='action_check', help='Commands for detecting/checking the GoPiGo3 board.')

fw_parser_actions = (
    'burn'
)
fw_parser.add_argument(action='store', choices=fw_parser_actions, dest='action_firmware', help='Command for burning the firmware on the GoPiGo3.')

shutdown_button_parser_actions = (
    'configure-shutdown-service',
    'uninstall-shutdown-service'
)
shutdown_button_parser.add_argument(action='store', choices=shutdown_button_parser_actions, dest='action_shutdown_button', help='Commands for configuring/uninstalling the shutdown button of the GoPiGo3.')
#############################################################

def main():
    # parsing command line arguments
    args = parser.parse_args()
    dict_args = vars(args)


    if args.version:
        import pkg_resources as pkg
        print("GoPiGo3-dev: " + pkg.get_distribution('gopigo3-dev').version)
    else:

        if 'action_command' in dict_args:
            from gopigo3 import easygopigo3 as easy

            # entered action subparser
            # this parser deals with controlling the GoPiGo3 (physically)

            try:
                robot = easy.EasyGoPiGo3()
            except IOError:
                print("The GoPiGo3 does not appear to be connected - command not issued.")
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

        elif 'action_check' in dict_args:
            pass
        elif 'action_firmware' in dict_args:
            pass
        elif 'action_shutdown_button' in dict_args:
            pass
        else:
            import pkg_resources as pkg
            from rst2ansi import rst2ansi
            readme_path = pkg.resource_filename('gopigo3', 'additional-files/README.rst')

            print('Enter "gopigo3 -h" or "gopigo3 --help" for instructions on how to use the command line to interface with the GoPiGo3\n')
            with open(readme_path, 'r') as f:
                print(rst2ansi(f.read().encode('utf-8')))


