
from .base import ROOT
from .results import Result


___all__ = ['NetworkControlCommand']





class _StatusConnectivityCommand(ROOT):
    """
       connectivity [check]
           Get network connectivity state.
           The optional check argument tells NetworkManager to re-check the connectivity, else the most recent known connectivity state is displayed without re-checking.

           Possible states are:
               none
                   the host is not connected to any network.

               portal
                   the host is behind a captive portal and cannot reach the full Internet.

               limited
                   the host is connected to a network, but it has no access to the Internet.

               full
                   the host is connected to a network and has full access to the Internet.

               unknown
                   the connectivity status cannot be found out.
    """
    NONE = 0
    PORTAL = 1
    LIMITED = 2
    FULL = 3
    UNKNOWN = 4

    state_descriptions = {
            "none":    "The host is not connected to any network.",
            "portal":  "The host is behind a captive portal and cannot reach the full Internet.",
            "limited": "The host is connected to a network, but it has no access to the Internet.",
            "full":    "The host is connected to a network and has full access to the Internet.",
            "unknown": "The connectivity status cannot be found out."
            }

    class sub_cmd(object):
        check = 'ifname'
    def __call__(self, check: bool = True) -> Result:
        return self._run_action(self.__base_command__, check)

    # def __init__(self): pass



class NetworkControlCommand(ROOT):
    """
    NETWORKING CONTROL COMMANDS
       nmcli networking {on | off | connectivity} [ARGUMENTS...]

       Query NetworkManager networking status, enable and disable networking.

       on, off
           Enable or disable networking control by NetworkManager. All interfaces managed by NetworkManager are deactivated when networking is disabled.
    """
    __base_command__: str = 'networking'
    class sub_cmd(object):
        on = 'on'
        off = 'off'
    def __init__(self):
        self.connectivity = _StatusConnectivityCommand(base=self.__base_command__)

    def on(self) -> Result:
        return self._run_action(self.__base_command__, self.sub_cmd.on)

    def off(self) -> Result:
        return self._run_action(self.__base_command__, self.sub_cmd.off)

    def __call__(self, *args, **kwargs) -> Result:
        return self._run_action(self.__base_command__, *args, **kwargs)

