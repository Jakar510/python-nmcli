
from .standard_parsers import *
from .base import *
from .results import Result


___all__ = ['GeneralCommand']





class _GeneralStatusCommand(ROOT):
    """
       status
           Show overall status of NetworkManager. This is the default action, when no additional command is provided for nmcli general.
    """
    __cmd__ = 'status'
    _status_parser = Parser(action=header_single_row_parser)

    def __call__(self) -> Result:
        """
        nmcli general
            STATE      CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
            connected  full          enabled  enabled  enabled  enabled

        :return:
        """
        return self._run_action(self.__base_command__, self.__cmd__, parser=self._status_parser)

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
    _hostname_parser = Parser(action=single_parser)

    def __call__(self) -> Result:
        """
            nmcli general hostname
                hostname

        :return:
        """
        return self._run_action(self.__base_command__, self.__cmd__, parser=self._hostname_parser)

class _GeneralPermissionsCommand(ROOT):
    """
       permissions
           Show the permissions a caller has for various authenticated operations that NetworkManager provides,
           like enable and disable networking, changing Wi-Fi and WWAN state, modifying connections, etc.
    """
    __cmd__ = 'permissions'

    # _parse(s)
    _status_parser = Parser(action=row_parser, column_names=['PERMISSION', 'VALUE'])

    def __call__(self) -> Result:
        """
            PERMISSION                                                        VALUE
            org.freedesktop.NetworkManager.enable-disable-network             no
            org.freedesktop.NetworkManager.enable-disable-wifi                no
            org.freedesktop.NetworkManager.enable-disable-wwan                no
            org.freedesktop.NetworkManager.enable-disable-wimax               no
            org.freedesktop.NetworkManager.sleep-wake                         no
            org.freedesktop.NetworkManager.network-control                    auth
            org.freedesktop.NetworkManager.wifi.share.protected               no
            org.freedesktop.NetworkManager.wifi.share.open                    no
            org.freedesktop.NetworkManager.settings.modify.system             no
            org.freedesktop.NetworkManager.settings.modify.own                auth
            org.freedesktop.NetworkManager.settings.modify.hostname           auth
            org.freedesktop.NetworkManager.settings.modify.global-dns         auth
            org.freedesktop.NetworkManager.reload                             auth
            org.freedesktop.NetworkManager.checkpoint-rollback                auth
            org.freedesktop.NetworkManager.enable-disable-statistics          no
            org.freedesktop.NetworkManager.enable-disable-connectivity-check  no

        :return:
        """
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

    @staticmethod
    def _parser(stdout: str) -> dict:
        l = stdout.strip().split('\n')[1].split()
        return {
                'LEVEL':  l[0].strip(),
                'DOMAINS':  l[1].split(',')
                }
    _logging_parser = Parser(action=_parser)
    def __call__(self) -> Result:
        """
            nmcli general logging
                LEVEL  DOMAINS
                INFO   PLATFORM,RFKILL,ETHER,WIFI,BT,MB,DHCP4,DHCP6,PPP,IP4,IP6,AUTOIP4,DNS,VPN,SHARING,SUPPLICANT,AGENTS,SETTINGS,SUSPEND,CORE,DEVICE,OLPC,INFINIBAND,FIREWALL,ADSL,BOND,VLAN,BRIDGE,TEAM,CONCHECK,DCB,DISPATCH,AUDIT,SYSTEMD,PROXY
        :param level:
        :param domains:
        :return:
        """
        return self._run_action(self.__base_command__, self.__cmd__, parser=self._logging_parser )

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
        """
        nmcli general
            STATE      CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
            connected  full          enabled  enabled  enabled  enabled
        :return:
        """
        return self.status()  # default command from man nmcli general


