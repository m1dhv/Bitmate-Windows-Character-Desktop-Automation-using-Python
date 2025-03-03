from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def mute_microphone():
    devices = AudioUtilities.GetMicrophone()
    if not devices:
        print("No microphone found")
        return
    
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set microphone volume to 0 (mute)
    volume.SetMasterVolumeLevelScalar(0.0, None)
    print("Microphone muted")

def unmute_microphone():
    devices = AudioUtilities.GetMicrophone()
    if not devices:
        print("No microphone found")
        return

    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Restore microphone volume to full (unmute)
    volume.SetMasterVolumeLevelScalar(1.0, None)
    print("Microphone unmuted")


            