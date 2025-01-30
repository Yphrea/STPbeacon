import datetime
import pexpect
import sys

#this is the mac address of the beacon
look_for_mac = "1C:1B:B5:77:54:10"

def scan_for_beacon(look_for_mac):
    proc = pexpect.spawn('bluetoothctl', encoding='utf-8')
    proc.expect(['bluetooth'])
    proc.sendline('menu scan')
    proc.sendline('duplicate-data on')
    proc.sendline('back')
    proc.sendline('scan on')

    last_detection = None
    while True:
        try:
            proc.expect('RSSI:', timeout=None) #look for advertisement signal strength
            try:
                mac = proc.before.split()[-1] #get mac address
                if not mac == look_for_mac:
                    continue
            except IndexError:
                continue
            proc.expect('\\n')
            rest_of_line = proc.before.split()
            #different versions of bluetoothctl uses a different formatting...
            if len(rest_of_line) == 1:
                RSSI = int(rest_of_line[0])
            elif len(rest_of_line) == 2:
                RSSI = rest_of_line[1].replace('(','')
                RSSI = rest_of_line[1].replace(')','')
                RSSI = int(RSSI)

            #time from last advertisement
            now = datetime.datetime.now()
            try:
                diff = now-last_detection
                print(mac, RSSI, diff)
            except TypeError:
                pass
            last_detection = now
                        
            sys.stdout.flush()
        except KeyboardInterrupt: #bluetoothctl runs interactively, this avoids unnessecary error message when killing the process
            print()
            break

scan_for_beacon(look_for_mac)
