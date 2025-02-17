#!/bin/bash

# Start advertising from bluetooth device on linux system

# See Bluetooth Core Specification (BCS) 4.0 vol 2 sec 7.8.7 (p. 816)
# Advertising flags
AD_FLAGS="02 01 1a"

# Beacon protocol. All items prefilled here cannot be edited, those which can are taken from the profile
AD_LENGTH="1b"
AD_TYPE="ff"
MFG_ID="18 01"
BEACON_CODE="be ac" #AltBeacon protocol
MFG_RESERVED="01"

# major and minor can be changed to indicate beacon identity
major="11 11"
minor="22 33"
BEACON_ID="$major $minor"
REFERENCE_RSSI="c5" #Reference RSSI at calibration distance (typically 1m). Not used. 

UUID="e2 0a 39 f4 73 f5 4b c4 a1 2f 17 d1 ad 07 a9 61"

Ad_Flags=`echo "$AD_FLAGS"`
Advertisement=`echo "$AD_LENGTH $AD_TYPE $MFG_ID $BEACON_CODE"`
Message=`echo "$UUID $BEACON_ID $REFERENCE_RSSI $MFG_RESERVED"`

# change to advertising device
# To see bluetooth devices available at your system, type "hcitool dev"
BLE="hci0"

# Turn off BLE
sudo hciconfig $BLE down

# Turn on BLE
sudo hciconfig $BLE up

# Set the Beacon
sudo hcitool -i $BLE cmd 0x08 0x0008 1f $Ad_Flags $Advertisement $Message

# set advertisement frequency (min and max first 4 bytes) and non-connectable mode (5th byte)
# Second to last byte sets advertisement channels, see BCS vol 2 sec 7.8.5 for more info
sudo hcitool -i $BLE cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00

# Start advertisement
sudo hcitool -i $BLE cmd 0x08 0x000a 01
