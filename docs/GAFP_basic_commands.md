# Gemini Astro Automatic Flat Panel V2
## Serial port specifications
- Serial Data Rate: 9600 Baud
- Parity：None
- StopBits：One
- DataBits：8
- DTR：false
- RTS：false
- ReceiveTimeout：5
## Basic Commands
|Send|Recieve|Description|
|----|-------|-----------|
|>H#|*HGeminiFlatPanel#|Used to find device|
|>V#|*Vvvv#|Get firmware version, must (vvv > 402)|
|>S#|*SidMLC#|Get device status(id =19 or 99)|
|||M = motor status( 0 stopped, 1 running)|
|||L = light status( 0 off, 1 on)|
|||C = Cover Status( 0 moving, 1 closed, 2 open, 3 timed out)|
|>Tx#|None|Turn on/off Beep ,x = 0 Off, x =1 On|
|>L#|*Lxxx#|Turn on light, xxx = 0 - 255|
|>D#|*Did#|Turn off light|
|>Bxxx#|*Bxxx#|Set brightness (xxx = 000-255)|
|>J#|*Jxxx#|Get brightness from device|
|>Yx#|None|Set Brightness Mode, x = 0 Low Bri, x = 1 High Bri|
|>O#|*OOpened#|Open cover|
|>C#|*CClosed#|Close cover|
|>A#|*Ax#|is ready? Is Opening and closing angle set? 0 NO, 1 Ready|
|>Mxxx#|NC|Move to xxx Position , xxx is angle , like -1, -10, -45 for closing|
|||1,10,45 for opening|
|>F#|NC|Set curr position as  Closed position.|
|>E#|NC|Set curr position as Opened position.|
