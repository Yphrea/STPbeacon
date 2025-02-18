import datetime
import pexpect
import sys

"""Scan for advertisement from supplied beacon mac address
using bluetoothctl on linux. Mac, RSSI and time stamp from
first recieved advertisement are printed to stdout.

Bluetoothctl is an interactive command line tool for
interacting with bluetooth devices on linux."""


#mac address of beacon to scan for
#look_for_mac = "1C:1B:B5:77:54:10" #Patchouli
#look_for_mac = "A0:A4:C5:EC:2A:AB" #Leyrien
#look_for_mac = "E4:A7:A0:A6:56:7A" #Juniper
#look_for_mac = "5C:F3:70:9C:02:DF" #dongle
look_for_mac = "cd:d7:e9:7e:31:9e".upper() #Nano 33 BLE

def scan_for_beacon(look_for_mac):
    proc = pexpect.spawn('bluetoothctl', encoding='utf-8')
    proc.expect(['bluetooth']) #wait for bluetoothctl to start
    proc.sendline('menu scan') #enter scan menu
    proc.sendline('duplicate-data on') #enable logging of every advertisement, not just the first one
    proc.sendline('back')
    proc.sendline('scan on')

    last_advertisement = None
    while True:
        try:
            proc.expect('RSSI:', timeout=None) #look for advertisement signal strength
            try:
                mac = proc.before.split()[-1]
                if not (mac == look_for_mac):
                    continue
            except IndexError:
                continue
            proc.expect('\\n')
            rest_of_line = proc.before.split()
            
            #different versions of bluetoothctl uses a different formatting:
            if len(rest_of_line) == 1:
                RSSI = int(rest_of_line[0])
            elif len(rest_of_line) == 2:
                RSSI = rest_of_line[1].replace('(','')
                RSSI = RSSI.replace(')','')
                RSSI = int(RSSI)


            try:
                now
            # If first data point, also log current time for use in data analysis
            except NameError:
                print(look_for_mac, 'start_time', datetime.datetime.now())
            now = datetime.datetime.now()
            
        
            try:
                diff = now-last_advertisement #time from last advertisement
                print(mac, RSSI, diff)
            except TypeError:
                print(mac, RSSI, now-now)
            last_advertisement = now
                        
            sys.stdout.flush()
            
        # catching error avoids error message when killing the process
        except KeyboardInterrupt: 
            print()
            break

scan_for_beacon(look_for_mac)
