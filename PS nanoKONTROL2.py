# Empty on purpose.
# FL Studio loads this file automatically.

import device

def OnInit():
    print("PS nanoKONTROL2 loaded")

    # CC 41 value 127
    device.midiOutMsg(0x0B, 0, 41, 127)