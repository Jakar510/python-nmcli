
from .base import ROOT
from .results import Result


___all__ = ['GeneralCommand']




class _GeneralStatusCommand(ROOT):
    """
       status
           Show overall status of NetworkManager. This is the default action, when no additional command is provided for nmcli general.
    """
    __cmd__ = 'status'
    def __call__(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__)

class _GeneralHostNameCommand(ROOT):
    """
       hostname [hostname]
           Get and change system hostname. With no arguments, this prints currently configured hostname.
           When you pass a hostname, it will be handed over to NetworkManager to be set as a new system hostname.

           Note that the term "system" hostname may also be referred to as "persistent" or "static" by other programs or tools.
           The hostname is stored in /etc/hostname file in most distributions.
           For example, systemd-hostnamed service uses the term "static" hostname and it only reads the /etc/hostname file when it starts.
    """
    __cmd__ = 'hostname'
    def __call__(self, host_name: str) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, host_name)

class _GeneralPermissionsCommand(ROOT):
    """
       permissions
           Show the permissions a caller has for various authenticated operations that NetworkManager provides,
           like enable and disable networking, changing Wi-Fi and WWAN state, modifying connections, etc.
    """
    __cmd__ = 'permissions'
    def __call__(self) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__)

class _GeneralLoggingCommand(ROOT):
    """
       logging [level level] [domains domains...]
           Get and change NetworkManager logging level and domains.
           Without any argument current logging level and domains are shown.
           In order to change logging state, provide level and, or, domain parameters.
           See NetworkManager.conf(5) for available level and domain values.

           TODO: finish implementation
    """
    __cmd__ = 'logging'
    class sub_cmd(object):
        level = 'level'
        domains = 'domains'
    def __call__(self, level, domains) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, kwargs={ self.sub_cmd.level: level, self.sub_cmd.domains: domains} )

class GeneralCommand(object):
    """
    GENERAL COMMANDS
       nmcli general {status | hostname | permissions | logging} [ARGUMENTS...]

       Use this command to show NetworkManager status and permissions. You can also get and change system hostname, as well as NetworkManager logging level and domains.
    """
    __base_command__: str = 'general'
    def __init__(self):
        self.status = _GeneralStatusCommand(base=self.__base_command__)
        self.hostname = _GeneralHostNameCommand(base=self.__base_command__)
        self.permissions = _GeneralPermissionsCommand(base=self.__base_command__)
        self.logging = _GeneralLoggingCommand(base=self.__base_command__)

    def __call__(self) -> Result:
        return self.status()


