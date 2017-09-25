import argparse
import pkg_resources as pkg

parser = argparse.ArgumentParser(description='This is a command-line tool for interfacing with the GoPiGo3 board\n'\
                                 'It can be used for:\n'\
                                 '1. Remotely controlling a GoPiGo3 robot.\n'\
                                 '2. Installing/Uninstalling the shutdown button support.\n'\
                                 '3. Checking the firmware and retrieving more info about it.\n'\
                                 '4. Flashing the firmware.',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-v', '--version', action='store_true', required=False, help='Retrieve the version of the GoPiGo3-dev pip package.')

subparsers = parser.add_subparsers(help='sub-command help')

go_parser = subparsers.add_parser('action', description='Sub-commands for controlling the GoPiGo3.')
check_parser = subparsers.add_parser('check', description='Sub-commands for checking the GoPiGo3.')
fw_parser = subparsers.add_parser('firmware', description='Firmware related stuff of the GoPiGo3.')
shutdown_button_parser = subparsers.add_parser('shutdown-button', description='Sub-commands for installing/uninstalling the shutdown button support.')

def main():
    args = parser.parse_args()
    if args.version:
        print("GoPiGo3-dev: " + pkg.get_distribution('gopigo3-dev').version)
    else:
        with open('../README.rst', 'r') as f:
            print(f.read())