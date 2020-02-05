
from .base import ROOT
from .results import Result


___all__ = ['RadioTransmissionControlCommand', 'MonitorCommand']



class MonitorCommand(ROOT):
    """
    ACTIVITY MONITOR
       nmcli monitor

       Observe NetworkManager activity. Watches for changes in connectivity state, devices or connection profiles.

       See also nmcli connection monitor and nmcli device monitor to watch for changes in certain devices or connections.
    """
    __base_command__: str = 'monitor'
    def __call__(self, *args, **kwargs) -> Result:
        return self._run_action(self.__base_command__, *args, **kwargs)

    def __init__(self):
        pass





class RTC_WiFi_Command(ROOT):
    """
       wifi [on | off]
           Show or set status of Wi-Fi in NetworkManager.
           If no arguments are supplied, Wi-Fi status is printed; on enables Wi-Fi; off disables Wi-Fi.
    """
    __cmd__ = 'wifi'
    class sub_cmd(object):
        on = 'on'
        off = 'off'

    def on(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.on)

    def off(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.off)



class RTC_WWan_Command(ROOT):
    """
       wwan [on | off]
           Show or set status of WWAN (mobile broadband) in NetworkManager.
           If no arguments are supplied, mobile broadband status is printed; on enables mobile broadband, off disables it.
    """
    __cmd__ = 'wwan'
    class sub_cmd(object):
        on = 'on'
        off = 'off'
    def on(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.on)

    def off(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.off)



class RTC_All_Command(ROOT):
    """
       all [on | off]
           Show or set all previously mentioned radio switches at the same time.
    """
    __cmd__ = 'all'
    class sub_cmd(object):
        on = 'on'
        off = 'off'
    def on(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.on)

    def off(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.off)



class RadioTransmissionControlCommand(object):
    """
    RADIO TRANSMISSION CONTROL COMMANDS
       nmcli radio {all | wifi | wwan} [ARGUMENTS...]

       Show radio switches status, or enable and disable the switches.
    """
    __base_command__: str = 'radio'
    def __init__(self):
        self.wifi = RTC_WiFi_Command(base=self.__base_command__)
        self.wwan = RTC_WWan_Command(base=self.__base_command__)
        self.all = RTC_All_Command(base=self.__base_command__)
