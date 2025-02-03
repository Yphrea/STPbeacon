#!/bin/bash

# Advertising flags
AD_FLAGS="02 01 1a"

# Beacon protocol. All items prefilled here cannot be edited, those which can are taken from the profile
AD_LENGTH="1b"
AD_TYPE="ff"
MFG_ID="18 01"
BEACON_CODE="be ac"
MFG_RESERVED="01"

major="11 11"
minor="22 33"
reference_rssi="c5"
BEACON_ID="$major $minor"
REFERENCE_RSSI="$reference_rssi"

UUID="e2 0a 39 f4 73 f5 4b c4 a1 2f 17 d1 ad 07 a9 61"
#UUID="e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0"

Ad_Flags=`echo "$AD_FLAGS"`
Advertisement=`echo "$AD_LENGTH $AD_TYPE $MFG_ID $BEACON_CODE"`
Message=`echo "$UUID $BEACON_ID $REFERENCE_RSSI $MFG_RESERVED"`

# Commands running on Raspberry Pi
BLE="hci0"

# Turn off BLE
sudo hciconfig $BLE down

# Turn on BLE
sudo hciconfig $BLE up

# Set the Beacon
sudo hcitool -i $BLE cmd 0x08 0x0008 1f $Ad_Flags $Advertisement $Message
#sudo hcitool -i $BLE cmd 0x08 0x0008 1f 02 01 1a 1a ff 4c 00 02 15 e2 c5 6d b5 df fb 48 d2 b0 60 d0 f5 a7 10 96 e0 00 00 00 00 c5 01
#sudo hcitool -i $BLE cmd 0x08 0x0008 1F 02 01 1A 1B FF 18 01 BE AC E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61 11 11 22 33 C5 01
sudo hcitool -i $BLE cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00 #set advertisement frequency (min and max first 4 bytes) and non-connectable mode (5th byte)
sudo hcitool -i $BLE cmd 0x08 0x000a 01
