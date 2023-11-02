#!/usr/bin/python3

# oxagast / Marshall Whittaker

import sys
import os
import time
import re
import uuid
import multiprocessing
import subprocess
import getpass
from bthid import BluetoothHIDService
from dbus.mainloop.glib import DBusGMainLoop

sys.tracebacklimit = 0  # this removes the traceback
btsrv = "bluetooth"
subprocess.call(["systemctl", "stop", btsrv])
subprocess.call(["bluetoothd", "-P", "input"])
waiting = 0
attackmac = (hex(uuid.getnode()+4).lstrip("0x").zfill(2).upper()) # gotta add 4 to get to the HID ctl otherwise proto wrong
attackmac = ':'.join(attackmac[i:i+2] for i in range(0, len(attackmac), 2))  # this just adds the : every 2 chars
print("[?] AntiLockDown by oxagast")
print("[?] Inhibits screensavers by pressing innoculous keys over bluetooth.")
if getpass.getuser() != "root":
    sys.stderr.write("[x] You need to run this program as root!\n")
    sys.exit(1)
print("[*] Attacking MAC detected as: %s" % attackmac)
def macr(send_call_back):
    def fkeys():
        j = 1
        while j:
            kstate = bytearray([0xA1, 0x01, 0x00, 0x00, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00])  # code to press shift+F10
            time.sleep(1)
            send_call_back(bytes(kstate))  # these actually send the keystroke
            kstate = bytearray([0xA1, 0x01, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00])  # code to press shift+F9
            send_call_back(bytes(kstate))
            time.sleep(15) # every 15 seconds so we're well within the screensaver timer
    def ani():
        waiting = 1
        idx = 0
        while waiting:
            animation = "|/-\\"  # we iterate over this
            print("[" + animation[idx % len(animation)] + "] Jiggling...", end='\r') # \r repositions the cursor at start
            idx+=1
            time.sleep(0.1)
    print("[!] Inhibiting lock screen on remote computer!")
    global st
    st = time.time()
    anip = multiprocessing.Process(target=ani) # the spinning animation thread
    jigp = multiprocessing.Process(target=fkeys) # pressing keys thread
    jigp.start()
    anip.start()
    jigp.join()
    anip.join()
if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    srec = open("sdpr.xml").read()
    try:
        bthid_srv = BluetoothHIDService(srec, attackmac)
        macr(bthid_srv.send)
    finally:
        if 'st' in globals():
            print("\n[*] Jiggled for %s seconds." % (time.time() - st))
        print("[x] Stopped.")
        sys.exit(0)
