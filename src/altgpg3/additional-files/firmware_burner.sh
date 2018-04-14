#!/usr/bin/env bash

openocd_installed='yes'

if ! { [ -f /usr/bin/openocd ] && [ -d /usr/local/share/openocd ]; }; then

    # Copy binaries if only the script was ran with the right permissions
    if [ -w /usr/local/share/ ] && [ -w /usr/bin/ ]; then
        # unzip the compiled OpenOCD
        unzip openocd_compiled.zip -d /tmp/openocd

        pushd /tmp/openocd
        cp -rn openocd_compiled/files/openocd /usr/local/share
        cp -rn openocd_compiled/openocd /usr/bin
        popd

        # Make the openocd binary executable
        chmod +x /usr/bin/openocd

        # Remove the unzipped files
        rm -rf /tmp/openocd
    else
        echo "Not enough permissions to install fw-related tools."
        echo "Check the command line's helper."
        openocd_installed='no'
    fi

fi

if [ $openocd_installed == 'yes' ] && if [ -w /usr/local/share/ ] && [ -w /usr/bin/ ]; then
    # Gets the absolute path of the latest Firmware update
    FW_UPDATE_FILE=$(find "$PWD"/ -maxdepth 1 -name *.bin)
    echo "Updating the GoPiGo3 Firmware with '$FW_UPDATE_FILE'."
    openocd -f interface/raspberrypi2-native.cfg -c "transport select swd; set CHIPNAME at91samc20j18; source [find target/at91samdXX.cfg]; adapter_khz 250; adapter_nsrst_delay 100; adapter_nsrst_assert_width 100" -c "init; targets; reset halt; program $FW_UPDATE_FILE verify; reset" -c "shutdown"
    exit 0
else
    echo "Not enough permissions to flash firmware to GoPiGo3."
    echo "Check the command line's helper."
    exit 1
fi
