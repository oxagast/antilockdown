#!/usr/bin/python3

# oxagast / Marshall Whittaker

import sys
import os
import time
import re
import uuid
import multiprocessing
from bthid import BluetoothHIDService
from dbus.mainloop.glib import DBusGMainLoop
sys.tracebacklimit = 0
#print (attackmac)
#attackmac = sys.argv[1]
start_time = time.time()
waiting = 0
attackmac = (hex(uuid.getnode()+4).lstrip("0x").zfill(2).upper()) # gotta add 4 to get to the HID ctl otherwise proto wrong
attackmac = ':'.join(attackmac[i:i+2] for i in range(0, len(attackmac), 2))  # this just adds the : every 2 chars
print("[?] Jiggalo by oxagast")
print("[?] Inhibits screensavers by pressing innoculous keys over bluetooth.")
print("[*] Attacking MAC detected as: %s" % attackmac)

def macr(send_call_back):
    def slpa():
        kstate = bytearray([0xA1, 0x00, 0x00, 0x00, 0x47, 0x00, 0x00, 0x00, 0x00, 0x00])  # nop
        time.sleep(1)
        send_call_back(bytes(kstate))
        kstate = bytearray([0xA1, 0x00, 0x00, 0x00, 0x48, 0x00, 0x00, 0x00, 0x00, 0x00])  # nop
        send_call_back(bytes(kstate))

    def fkeys():
        j = 1
        while j:
            kstate = bytearray([0xA1, 0x01, 0x00, 0x00, 0x43, 0x00, 0x00, 0x00, 0x00, 0x00])  # nop
            time.sleep(1)
            send_call_back(bytes(kstate))
            kstate = bytearray([0xA1, 0x01, 0x00, 0x00, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00])  # nop
            send_call_back(bytes(kstate))
            time.sleep(15)

    def ani():
        waiting = 1;
        idx = 0
        while waiting:
            animation = "|/-\\"
            print(animation[idx % len(animation)], end='\r')
            idx+=1
            time.sleep(0.1)

    print("[!] Inhibiting lock screen on remote computer!")
    jiggle = 1
    anip = multiprocessing.Process(target=ani)
    jigp = multiprocessing.Process(target=fkeys)
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
        print("\n[*] Jiggled for %s seconds." % (time.time() - start_time))
        print("[x] Jiggling stopped.")
