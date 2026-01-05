from serial import Serial
import sys
from subprocess import Popen, PIPE
from typing import List
import time

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def fancy_print(text_type, text):
    """uses the bcolors class to color code text output for readability
    text_type: bcolors value for text output color
    text: text to be printed in the terminal window"""
    print(f"{text_type}{text}{bcolors.ENDC}")

def run_command(command: List[str]) -> str:
    """runs a given text command in the terminal window and prints the output and any errors
    command: single command in a list to run"""
    fancy_print(bcolors.OKBLUE, f"\nRunning command: {' '.join(command)}")
    output = ""

    process = Popen(command, stdout=PIPE, universal_newlines=True)

    # Read and print the output line by line while the command is running
    for line in process.stdout:
        print(line, end="")
        output += line

    # Wait for the command to finish running
    return_code = process.wait()

    #assert return_code == 0, f"Command execution failed with return code: {return_code}"

    return output


sources = {
    "xray_sources": [
            # 120 kV VJX
            {
                "serialIdentifier": "673",
                "horizontalCropPercent": 90,
                "kvMin": 40,
                "kvMax": 120,
                "uaMin": 50,
                "uaMax": 300,
                "settingsModel": "IXS120BP036P112",
            },
            {
                "serialIdentifier": "649",
                "horizontalCropPercent": 85,
                "kvMin": 40,
                "kvMax": 120,
                "uaMin": 50,
                "uaMax": 300,
                "settingsModel": "IXS120BP036P112",
            },
            {
                "serialIdentifier": "112",
                "horizontalCropPercent": 85,
                "kvMin": 40,
                "kvMax": 120,
                "uaMin": 50,
                "uaMax": 300,
                "settingsModel": "IXS120BP036P112",
            },
            # 120 kV P673 with Luxbright tube
            {
                "serialIdentifier": "796",
                "horizontalCropPercent": 90,
                "kvMin": 40,
                "kvMax": 120,
                "uaMin": 50,
                "uaMax": 300,
                "settingsModel": "IXS120BP036P112",
            },
            # 120 kV VJX DC P755
            {
                "serialIdentifier": "755",
                "horizontalCropPercent": 90,
                "kvMin": 80,
                "kvMax": 120,
                "uaMin": 200,
                "uaMax": 800,
                "settingsModel": "IXS120BP096P755",
            },
            # 160 kV VJX DC P747
            {
                "serialIdentifier": "747",
                "horizontalCropPercent": 90,
                "kvMin": 80,
                "kvMax": 160,
                "uaMin": 200,
                "uaMax": 625,
                "settingsModel": "IXS160BP100P747",
            },
            # 190 kV VJX
            {
                "serialIdentifier": "401",
                "horizontalCropPercent": 90,
                "kvMin": 100,
                "kvMax": 190,
                "uaMin": 200,
                "uaMax": 500,
                "settingsModel": "IXS200BP150P401",
            },
            {
                "serialIdentifier": "643",
                "horizontalCropPercent": 90,
                "kvMin": 100,
                "kvMax": 190,
                "uaMin": 200,
                "uaMax": 500,
                "settingsModel": "IXS200BP150P401",
            },
            # 320 kV VJX
            {
                "serialIdentifier": "662",
                "horizontalCropPercent": 90,
                "kvMin": 160,
                "kvMax": 320,
                "uaMin": 500,
                "uaMax": 2500,
                "settingsModel": "IXS320BP800P662",
            },
            # # 130 kV Hamamatsu (this doesn't Exist!)
            # {
            #     "serialIdentifier": None,
            #     "horizontalCropPercent": 100,
            #     "kvMin": 40,
            #     "kvMax": 130,
            #     "uaMin": 0,
            #     "uaMax": 300,
            #     "settingsModel": "L9181-02",
            # },
        ],
}


def get_return_SNUM():
    """
    Retrieves the firmware string from a serial device.
    This function attempts to connect to a serial device on a specified port (default is "/dev/ttyUSBXRAY")
    and sends a command to retrieve the firmware ID. The firmware ID is expected to be the first 4 characters
    of the response.
    Returns:
        str: The firmware type string (first 4 characters of the response: the firmware version).
    Notes:
        - The function reads from the serial port until a carriage return (0x0D) is encountered or the buffer size reaches 255 bytes.
        - If no data is received, the loop exits.
        - The function handles exceptions and keyboard interrupts gracefully, printing the exception message.
        - The port can be specified as a command-line argument; otherwise, it defaults to "/dev/ttyUSBXRAY".
    """
    _PACKET_START = b"\x02"  # STX
    _PACKET_END = b"\x0D"  # CR
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "/dev/ttyUSBXRAY"
    firmware = ""
    ser = Serial(port, timeout=0.1)
    print("Type a message to send and press enter, or type \"quit\" to exit")
    try:
        cmd = "SNUM"
        model = ""
        ser.write(_PACKET_START + cmd.encode("ascii") + _PACKET_END)
        
        while True:
            rx = ser.read_until(terminator=b"\x0D", size=255)
            SNUM = rx.decode("ascii").strip().replace("\x02", "")            
            if not rx:
                break
            
            raise Exception("quit")
        
        
    except (Exception, KeyboardInterrupt) as e:
        print(e)
    finally:
        ser.close()
    for source in sources["xray_sources"]:
            if source["serialIdentifier"] in SNUM:
                model = source["settingsModel"]
                print("Source Type found!")
                print(model)
                print("kV range", source["kvMin"], " - ", source["kvMax"])
                print("uA range", source["uaMin"], " - ", source["uaMax"])
                break
    with open("model_output_file.txt", "w") as f:
        f.write(model)
    return model

def flash_homer(cfg=None) -> None:
    with open('/etc/homer_firmware_variant', 'r+') as homer_variant:
        variant = homer_variant.read().strip()
        homer_variant.seek(0)
        # if cfg != None:
        #     homer_variant.write(cfg)
        if variant == "+cfg15":
            homer_variant.write("+cfg11")
            source_type = "AC"
        else:
            homer_variant.write("+cfg15")
            source_type = "DC"
    run_command(['flash-homer-firmware'])
    print(f"Homerboard flashed to {source_type} style source. Previous type was {variant}.")

def prep_for_condition():
    # kill any old seah's running
    run_command(['pkill', 'seah'])
    delete_warming = ''
    # delete warming file?
    # delete_warming = input("Press 'Enter' to launch Seah")
    # if delete_warming.lower() == 'xray': 
    #     fancy_print(bcolors.WARNING, "You have chosen to use the last X-Ray on date to determine warming! Only do this for testing pre-warmed sources!")
    # elif delete_warming.lower() == 'photon':
    #     # TODO: add command to skip warming
    #     print("nothing happened")
    #     time.sleep(2)
    # else:
    run_command(["rm", "/var/seah/vjx_usage_history.json"])
    fancy_print(bcolors.OKCYAN, "Warming reset, please warm the source when Seah launches...")
    time.sleep(2)

def main():
    # Check if source is connected
    count = 0
    model = get_return_SNUM()
    # time.sleep(1)
    # while model == '' and count < 3:
    #     model = get_return_SNUM()
    #     flash_homer()
    #     count += 1
    # if count == 3:
    #     print("Error: Source not connected, please check the source is plugged in and all interlocks are closed")
    #     return
    # Prep for Conditioning
    prep_for_condition()
    return model
    
main()
