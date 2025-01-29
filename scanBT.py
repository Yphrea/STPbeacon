import subprocess
import shlex
import re
import time
import datetime
import pexpect, sys
from matplotlib import pyplot as plt


"""
Provides features for scanning for BLE beacon, identifying and printing relevant information.
Hopefully data will eventually be saved and processed but that's not here yet. 
"""


#Colors for coloring terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#shellcmd = shlex.split("{   printf 'scan on\\n';     sleep 2;     printf5'devices\\n';     printf 'quit\\n'; } | bluetoothctl")


mac = "0C:19:F8:96:13:D2" #mac address of desired BLE decive
mac = "80:7B:3E:27:69:CF" #mac address of desired BLE decive
mac = "5C:F3:70:9C:02:DF"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') #regex for removing color coding before interpreting process output

def BTscan_bluetoothctl():
    """Scan using bluetoothctl"""
    
    proc = pexpect.spawn('bluetoothctl', encoding='utf-8')
    proc.expect(['bluetooth'])
    proc.sendline('menu scan')
    proc.sendline('duplicate-data on')
    proc.sendline('back')
    proc.sendline('scan on')

    def collect_data():
        time = []; RSSI = []
        while True:
            try:
                proc.expect(mac, timeout=None)
                proc.expect('RSSI', timeout=1)
                try:
                    proc.before.split()[-1]
                    continue
                except IndexError:
                    time.append(datetime.datetime.now())
                    print('.', end='')
                proc.expect('\\)')
                RSSI.append(proc.before[proc.before.index('(')+1:])
                sys.stdout.flush()
            except KeyboardInterrupt: #bluetoothctl runs interactively, this avoids unnessecary error message when killing the process
                print()
                break        
    
        RSSI = [int(i) for i in RSSI]
        start_time = time[0]
        time = [t-start_time for t in time]
        time = [t.seconds + t.microseconds for t in time]
        plt.plot(time, RSSI, '*')
        plt.show()

    def find_close(threshold=-100, lookfor_mac = None):
        macs = []
        lasttime = datetime.datetime.now()
        while True:
            try:
                proc.expect('RSSI', timeout=None)
                try:
                    mac = proc.before.split()[-1]
                except IndexError:
                    continue
                proc.expect('\\)')
                RSSI = int(proc.before[proc.before.index('(')+1:])

                if RSSI >= threshold and ':' in mac:
                    if mac == lookfor_mac or lookfor_mac==None:
                        macs.append(mac)
                        now = datetime.datetime.now()
                        diff = now-lasttime
                        print(mac, RSSI, diff)
                        lasttime = now
                        
                sys.stdout.flush()
            except KeyboardInterrupt: #bluetoothctl runs interactively, this avoids unnessecary error message when killing the process
                print()
                break

    #stop chaning indentation python..
    find_close(-100, lookfor_mac = mac)
    #find_close(-60)
        
                
            

def BTscan_btmgmt():
    """Scan using btmgmt"""
    proc = subprocess.Popen(['sudo','btmgmt','--timeout','60','find'], stdout=subprocess.PIPE, universal_newlines=True)
    #proc = subprocess.Popen(['sudo','btmgmt','--timeout','60','find'], universal_newlines=True)
    #proc = subprocess.Popen(['sudo','btmgmt','advmon','on','&&','sudo','btmgmt','--timeout','60','find'], universal_newlines=True)
    print('looking for:',mac)
    
    try:
        while proc.poll()!=0: #is process proc (the scane) still running?
            for line in proc.stdout: #continuous monitoring of scan output
                line=line.split()
                print(line)
                try:
                    if 'rssi' in line and int(line[line.index('rssi')+1]) > -75:
                        print(line[0:-1], datetime.datetime.now())
                except IndexError:
                    pass
                except ValueError:
                    pass
                
            time.sleep(.5)
    except KeyboardInterrupt:
        exit()
        
    
#BTscan_btmgmt()
BTscan_bluetoothctl()


#the following seems to do the same as "bluetoothctl show":
#import pydbus
#bus = pydbus.SystemBus()
#obj_mngr = bus.get('org.bluez', '/')
#mngd_objs = obj_mngr.GetManagedObjects()
#for path, obj in mngd_objs.items():
#    for key, item in obj.items():
#        #print(key, item)
#        for keyy, itemm in item.items():
#            print(keyy, itemm)
