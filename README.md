# AntiLockDown
Inhibit a screensaver/lock screen via Bluetooth (also known as a *Jiggler*)

Author: oxagast

This is a simple program that will inhibit the screen locking on any Linux or Windows machine that
connects to it via Bluetooth by making somewhat innoculous keystrokes that keep the screen's timer
from ever reaching the set lockdown time.  The keystrokes, known as jiggles (this refers to simply
jiggling the mouse to keep the screen unlocked) are hard coded, and default o Shift+F9 and Shift+F10,
alternated, and this happens every 15 seconds to keep it well below any screen's set lock time.

The program takes no arguments, and the output resembles:

```
$ ./ald-jiggle.py
[?] AntiLockDown v1.1 by oxagast                                                                                                                                                                                                                        
[?] Inhibits screensavers by pressing innoculous keys over bluetooth.                                                                                                                                                                                   
[*] Attacking MAC detected as: DC:53:60:6C:FC:B3                                                                                                                                                                                                        
[*] Registered HID profile                                                                                                                                                                                                                              
[!] Ready, waiting for connection from PC to inhibit screensaver on...                                                                                                                                                                                  
[*] Control channel connected to 00:15:83:FA:12:FC                                                                                                                                                                                                      
[*] Interrupt channel connected to 00:15:83:FA:12:FC                                                                                                                                                                                                    
[!] Inhibiting lock screen on remote computer!                                                                                                                                                                                                          
[*] Press Ctrl+C to stop!                                                                                                                                                                                                                                 
^C                                                                                                                                                                                                                                                        
[*] Jiggled for 13.99 seconds.                                                                                                                                                                                                                            
[x] Signal caught, jiggling stopped.
```

Once started, you simply open the victim computer's Bluetooth menu, pair, and connect to the attacking machine.
When it is ready for your connection it will tell you, then continuously send the keystrokes, or jiggles, until
stopped (Ctrl+C kills the program cleanly), or on client disconnect.  It will show you how long it stopped the
screensaver from popping up.
