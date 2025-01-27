#!/bin/bash

# Script originally from the bluetooth tutorial Developer-Study-Guide-An-introduction-to-Bluetooth-BeaconsV1_3_4
# https://www.bluetooth.com/bluetooth-resources/bluetooth-le-developer-starter-kit/

# Advertising flags
AD_FLAGS="02 01 1a"

# Beacon protocol. All items prefilled here cannot be edited, those which can are taken from the profile
AD_LENGTH="1b"
AD_TYPE="ff"
MFG_ID="18 01"
BEACON_CODE="be ac" # Specific for AltBeacon BLE protocol
MFG_RESERVED="01"

major="11 11" # This can be used to encode information
minor="22 33" # This as well
reference_rssi="c5" #reference signal strength at 1m from beacon. I don't know what this should be and I don't think we need it
BEACON_ID="$major $minor"
REFERENCE_RSSI="$reference_rssi"

UUID="e2 0a 39 f4 73 f5 4b c4 a1 2f 17 d1 ad 07 a9 61"

Ad_Flags=`echo "$AD_FLAGS"`
Advertisement=`echo "$AD_LENGTH $AD_TYPE $MFG_ID $BEACON_CODE"`
Message=`echo "$UUID $BEACON_ID $REFERENCE_RSSI $MFG_RESERVED"`

# Commands running on Raspberry Pi
BLE="hci0"

# Turn off BLE
sudo hciconfig $BLE down

# Turn on BLE
sudo hciconfig $BLE up

# Stop LE advertising
sudo hciconfig $BLE noleadv

# Start LE advertising (option '3' implies non-connectable)
sudo hciconfig $BLE leadv 3

# Turn scanning off (can sometimes affect advertising)
sudo hciconfig $BLE noscan

# Set the Beacon
# the ocg and ocf 0x08 and 0x0008 indicates BLE protocol and LE-set-advertising-data--command (7.8.7 vol 2 in bluetooth 4.0 core specification), respectively
sudo hcitool -i $BLE cmd 0x08 0x0008 1f $Ad_Flags $Advertisement $Message

#sudo hcitool -i $BLE cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 00 00 c5

# Initiate advertisement using blutoothctl non-interactively
echo -e advertise on | bluetoothctl
