import os
import platform

def get_current_volume():
    system = platform.system()

    if system == 'Windows':
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            current_volume = volume.GetMasterVolumeLevel()
            return current_volume
        except ImportError:
            print("pycaw not install. Install this with 'pip install pycaw'")
    
    elif system == 'Darwin': 
        try:
            result = os.popen("osascript -e 'output volume of (get volume settings)'").read()
            return int(result.strip())
        except Exception as e:
            print(f"Error while getting config of music: {e}")
    
    elif system == 'Linux':
        try:
            result = os.popen("amixer get Master | grep 'Mono:' | awk -F'[][]' '{ print $2 }'").read()
            return result.strip()
        except Exception as e:
            print(f"Error while getting config of music: {e}")

    else:
        print(f"system{system} doesn't support your system")
        return None

current_volume = get_current_volume()
if current_volume is not None:
    print(f'Current volume: {current_volume}')




