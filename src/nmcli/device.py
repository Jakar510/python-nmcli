from .base import *
from .results import Result
from .standard_parsers import *




___all__ = ['DeviceCommand']

class _DevStatusCommand(ROOT):
    """
       status
           Print status of devices.

           This is the default action if no command is specified to nmcli device.
    """
    __cmd__ = 'status'

    @staticmethod
    def _parser(stdout: str, headers: list or tuple) -> dict:
        l = []
        for row in stdout.strip().split('\n'):
            if any(header in row for header in headers): continue
            l.append(row.split())

        d = { }
        for row in l:
            print(row)
            DEVICE, TYPE, STATE, *CONNECTION = row
            d[DEVICE] = {
                    'TYPE':       TYPE,
                    'STATE':      STATE,
                    'CONNECTION': ' '.join(CONNECTION),
                    }
        return d

    _status_parser = Parser(action=_parser, column_names=['DEVICE', 'TYPE', 'STATE', 'CONNECTION'])
    def __call__(self) -> Result:
        """
            nmcli device status
                DEVICE  TYPE      STATE      CONNECTION
                eth0    ethernet  connected  Wired connection 1
                wlan0   wifi      connected  Steggi
                lo      loopback  unmanaged  --

        :return:
        """
        return self._run_action(self.__base_command__, self.__cmd__)

class _DevShowCommand(ROOT):
    """
       show [ifname]
           Show detailed information about devices. Without an argument, all devices are examined. To get information for a specific device, the interface name has to be provided.
    """
    __cmd__ = 'show'

    @staticmethod
    def _parser(stdout: str) -> dict:
        device = ''
        temp = []
        for row in stdout.split('\n'):
            temp.append(anti_spacer.sub(' ', row).split(':', maxsplit=1))

        d = { }
        for row in temp:
            if row == ['']: continue
            key, value = row
            if "GENERAL.DEVICE" in key:
                device = value.strip()
                d[device] = {}
            d[device][key.strip()] = value.strip()
        return d

    _show_parser = Parser(action=_parser)
    def __call__(self) -> Result:
        """
        nmcli device show
            GENERAL.DEVICE:                         eth0
            GENERAL.TYPE:                           ethernet
            GENERAL.HWADDR:                         00:00:00:00:00:00
            GENERAL.MTU:                            1500
            GENERAL.STATE:                          100 (connected)
            GENERAL.CONNECTION:                     Wired connection 1
            GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/3
            WIRED-PROPERTIES.CARRIER:               on
            IP4.ADDRESS[1]:                         192.168.1.219/24
            IP4.GATEWAY:                            192.168.1.1
            IP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 100
            IP4.ROUTE[2]:                           dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 100
            IP4.DNS[1]:                             1.1.1.1
            IP4.DNS[2]:                             192.168.1.1
            IP6.ADDRESS[1]:                         fe80::680:d91:e7db:4635/64
            IP6.GATEWAY:                            --
            IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 100
            IP6.ROUTE[2]:                           dst = ff00::/8, nh = ::, mt = 256, table=255

            GENERAL.DEVICE:                         wlan0
            GENERAL.TYPE:                           wifi
            GENERAL.HWADDR:                         00:00:00:00:00:00
            GENERAL.MTU:                            1500
            GENERAL.STATE:                          100 (connected)
            GENERAL.CONNECTION:                     Steggi
            GENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/4
            IP4.ADDRESS[1]:                         192.168.1.157/24
            IP4.GATEWAY:                            192.168.1.1
            IP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 600
            IP4.ROUTE[2]:                           dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 600
            IP4.DNS[1]:                             1.1.1.1
            IP4.DNS[2]:                             192.168.1.1
            IP6.ADDRESS[1]:                         fe80::6e39:a7d1:bf1b:9f8a/64
            IP6.GATEWAY:                            --
            IP6.ROUTE[1]:                           dst = fe80::/64, nh = ::, mt = 600
            IP6.ROUTE[2]:                           dst = ff00::/8, nh = ::, mt = 256, table=255

            GENERAL.DEVICE:                         lo
            GENERAL.TYPE:                           loopback
            GENERAL.HWADDR:                         00:00:00:00:00:00
            GENERAL.MTU:                            65536
            GENERAL.STATE:                          10 (unmanaged)
            GENERAL.CONNECTION:                     --
            GENERAL.CON-PATH:                       --
            IP4.ADDRESS[1]:                         127.0.0.1/8
            IP4.GATEWAY:                            --
            IP6.ADDRESS[1]:                         ::1/128
            IP6.GATEWAY:                            --
            IP6.ROUTE[1]:                           dst = ::1/128, nh = ::, mt = 256

        :param ifname: {
                'eth0': {
                        'GENERAL.DEVICE': 'eth0',
                        'GENERAL.TYPE': 'ethernet',
                        'GENERAL.HWADDR': '00:00:00:00:00:00',
                        'GENERAL.MTU': '1500',
                        'GENERAL.STATE': '100 (connected)',
                        'GENERAL.CONNECTION': 'Wired connection 1',
                        'GENERAL.CON-PATH': '/org/freedesktop/NetworkManager/ActiveConnection/3',
                        'WIRED-PROPERTIES.CARRIER': 'on',
                        'IP4.ADDRESS[1]': '192.168.1.219/24',
                        'IP4.GATEWAY': '192.168.1.1',
                        'IP4.ROUTE[1]': 'dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 100',
                        'IP4.ROUTE[2]': 'dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 100',
                        'IP4.DNS[1]': '1.1.1.1',
                        'IP4.DNS[2]': '192.168.1.1',
                        'IP6.ADDRESS[1]': 'fe80::680:d91:e7db:4635/64',
                        'IP6.GATEWAY': '--',
                        'IP6.ROUTE[1]': 'dst = fe80::/64, nh = ::, mt = 100',
                        'IP6.ROUTE[2]': 'dst = ff00::/8, nh = ::, mt = 256, table=255'
                        },
                'wlan0': {
                        'GENERAL.DEVICE': 'wlan0',
                        'GENERAL.TYPE': 'wifi',
                        'GENERAL.HWADDR': '00:00:00:00:00:00',
                        'GENERAL.MTU': '1500',
                        'GENERAL.STATE': '100 (connected)',
                        'GENERAL.CONNECTION': 'Steggi',
                        'GENERAL.CON-PATH': '/org/freedesktop/NetworkManager/ActiveConnection/4',
                        'IP4.ADDRESS[1]': '192.168.1.157/24',
                        'IP4.GATEWAY': '192.168.1.1',
                        'IP4.ROUTE[1]': 'dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 600',
                        'IP4.ROUTE[2]': 'dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 600',
                        'IP4.DNS[1]': '1.1.1.1',
                        'IP4.DNS[2]': '192.168.1.1',
                        'IP6.ADDRESS[1]': 'fe80::6e39:a7d1:bf1b:9f8a/64',
                        'IP6.GATEWAY': '--',
                        'IP6.ROUTE[1]': 'dst = fe80::/64, nh = ::, mt = 600',
                        'IP6.ROUTE[2]': 'dst = ff00::/8, nh = ::, mt = 256, table=255'
                        },
                'lo': {
                        'GENERAL.DEVICE': 'lo',
                        'GENERAL.TYPE': 'loopback',
                        'GENERAL.HWADDR': '00:00:00:00:00:00',
                        'GENERAL.MTU': '65536',
                        'GENERAL.STATE': '10 (unmanaged)',
                        'GENERAL.CONNECTION': '--',
                        'GENERAL.CON-PATH': '--',
                        'IP4.ADDRESS[1]': '127.0.0.1/8',
                        'IP4.GATEWAY': '--',
                        'IP6.ADDRESS[1]': '::1/128',
                        'IP6.GATEWAY': '--',
                        'IP6.ROUTE[1]': 'dst = ::1/128, nh = ::, mt = 256'
                    }
             }

        :return:
        """
        return self._run_action(self.__base_command__, self.__cmd__, parser=self._show_parser)

class _DevSetCommand(ROOT):
    """
       set [ifname] ifname [autoconnect {yes | no}] [managed {yes | no}]
           Set device properties.
    """
    __cmd__ = 'set'

    class sub_cmd(object):
        autoconnect = 'autoconnect'
        managed = 'managed'
        yes = 'yes'
        no = 'no'

    def __call__(self, ifname: str, *, managed: bool = None, auto_connect: bool = None) -> Result:
        kwargs = { }
        if ifname is not None: kwargs[self.sub_cmd.ifname] = self.sub_cmd.yes if ifname else self.sub_cmd.no
        if managed is not None: kwargs[self.sub_cmd.managed] = self.sub_cmd.yes if managed else self.sub_cmd.no
        if auto_connect is not None: kwargs[self.sub_cmd.autoconnect] = self.sub_cmd.yes if auto_connect else self.sub_cmd.no
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)



class _DevConnectCommand(ROOT):
    """
       connect ifname
           Connect the device. NetworkManager will try to find a suitable connection that will be activated. It will also consider connections that are not set to auto connect.

           If --wait option is not specified, the default timeout will be 90 seconds.
    """
    __cmd__ = 'connect'

    @staticmethod
    def _parser(stdout: str) -> dict:
        device = ''
        temp = []
        for row in stdout.split('\n'):
            temp.append(anti_spacer.sub(' ', row).split(':', maxsplit=1))

        d = { }
        for row in temp:
            if row == ['']: continue
            key, value = row
            if "GENERAL.DEVICE" in key:
                device = value.strip()
                d[device] = {}
            d[device][key.strip()] = value.strip()
        return d

    _connect_parser = Parser(action=_parser)
    def __call__(self, if_name: str, wait: bool) -> Result:
        args = [if_name]
        if wait: args.append('--wait')
        return self._run_action(self.__base_command__, self.__cmd__, *args)



class _DevReapplyCommand(ROOT):
    """
       reapply ifname
           Attempt to update device with changes to the currently active connection made since it was last applied.
    """
    __cmd__ = 'reapply'



    class sub_cmd(object):
        ifname = 'ifname'



    def __call__(self, ifname: str = None) -> Result:
        kwargs = { self.sub_cmd.ifname: ifname }
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _DevModifyCommand(ROOT):
    """
       modify ifname {option value | [+|-]setting.property value}...  TODO: finish implementation
           Modify the settings currently active on the device.

           This command lets you do temporary changes to a configuration active on a particular device. The changes are not preserved in the connection profile.

           See nm-settings(5) for the list of available properties. Please note that some properties can't be changed on an already connected device.

           You can also use the aliases described in PROPERTY ALIASES section. The syntax is the same as of the nmcli connection modify command.
    """
    __cmd__ = 'modify'



    class sub_cmd(object):
        wait = '--wait'
        ifname = 'ifname'



    def __call__(self, ifname: str = None, *args, **kwargs) -> Result:
        raise NotImplementedError()

class _DevDisconnectCommand(ROOT):
    """
       disconnect ifname...
           Disconnect a device and prevent the device from automatically activating further connections without user/manual intervention. Note that disconnecting software devices may mean that the devices will disappear.

           If --wait option is not specified, the default timeout will be 10 seconds.
    """
    __cmd__ = 'disconnect'



    class sub_cmd(object):
        wait = '--wait'
        ifname = 'ifname'



    def __call__(self, ifname: str = None, wait: int = None) -> Result:
        kwargs = { self.sub_cmd.ifname: ifname }
        if wait: kwargs[self.sub_cmd.wait] = wait
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _DevDeleteCommand(ROOT):
    """
       delete ifname...
           Delete a device. The command removes the interface from the system. Note that this only works for software devices like bonds, bridges, teams, etc. Hardware devices (like Ethernet) cannot be deleted by the command.

           If --wait option is not specified, the default timeout will be 10 seconds.
    """
    __cmd__ = 'delete'



    class sub_cmd(object):
        wait = '--wait'
        ifname = 'ifname'



    def __call__(self, ifname: str = None, wait: int = None) -> Result:
        kwargs = { self.sub_cmd.ifname: ifname }
        if wait: kwargs[self.sub_cmd.wait] = wait
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _Dev_lldp_Command(ROOT):
    """
       lldp [list [ifname ifname]]
           Display information about neighboring devices learned through the Link Layer Discovery Protocol (LLDP).
           The ifname option can be used to list neighbors only for a given interface.
           The protocol must be enabled in the connection settings.
    """
    __cmd__ = 'lldp'



    class sub_cmd(object):
        list = 'list'
        ifname = 'ifname'



    def __call__(self, get_list: bool = None, if_name: str = None) -> Result:
        if get_list:
            return self._run_action(self.__base_command__, self.__cmd__, self.sub_cmd.list, kwargs={ self.sub_cmd.ifname: if_name })
        else:
            return self._run_action(self.__base_command__, self.__cmd__)

class _DevMonitorCommand(ROOT):
    """
       monitor [ifname...]
           Monitor device activity. This command prints a line whenever the specified devices change state.

           Monitors all devices in case no interface is specified. The monitor terminates when all specified devices disappear. If you want to monitor device addition consider using the global monitor with nmcli monitor command.
    """
    __cmd__ = 'monitor'



    class sub_cmd(object):
        ifname = 'ifname'



    def __call__(self, if_name: str = None) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, kwargs={ self.sub_cmd.ifname: if_name })

class WiFi_DevConnectCommand(ROOT):
    """
       wifi connect (B)SSID [password password] [wep-key-type {key | phrase}] [ifname ifname] [bssid BSSID] [name name] [private {yes | no}] [hidden {yes | no}]
           Connect to a Wi-Fi network specified by SSID or BSSID.
           The command creates a new connection and then activates it on a device.
           This is a command-line counterpart of clicking an SSID in a GUI client.
           The command always creates a new connection and thus it is mainly useful for connecting to new Wi-Fi networks.
           If a connection for the network already exists, it is better to bring up (activate) the existing connection as follows: nmcli con up id name.
           Note that only open, WEP and WPA-PSK networks are supported at the moment.
           It is also supposed that IP configuration is obtained via DHCP.

           If --wait option is not specified, the default timeout will be 90 seconds.

           Available options are:

           password
               password for secured networks (WEP or WPA).

           wep-key-type
               type of WEP secret, either key for ASCII/HEX key or phrase for passphrase.

           ifname
               interface that will be used for activation.

           bssid
               if specified, the created connection will be restricted just for the BSSID.

           name
               if specified, the connection will use the name (else NM creates a name itself).

           private
               if set to yes, the connection will only be visible to the user who created it. Otherwise the connection is system-wide, which is the default.

           hidden
               set to yes when connecting for the first time to an AP not broadcasting its SSID. Otherwise the SSID would not be found and the connection attempt would fail.
    """
    __cmd__ = 'connect'



    class sub_cmd(object):
        yes = 'yes'
        no = 'no'
        ifname = 'ifname'
        ssid = 'ssid'
        wait = '--wait'
        password = 'password'
        bssid = 'bssid'
        name = 'name'
        private = 'private'
        hidden = 'hidden'
        wep_key_type = 'wep-key-type'



    def __call__(self, if_name: str = None, password: str = None, wep_key_type: str = None, ssid: str = None, bssid: str = None, name: str = None,
                 private: bool = None, hidden: bool = None, wait: int = None) -> Result:
        args = []
        kwargs = { }
        if if_name is not None: kwargs[self.sub_cmd.ifname] = if_name
        if ssid is not None: kwargs[self.sub_cmd.ssid] = ssid
        if password is not None: kwargs[self.sub_cmd.password] = password
        if wep_key_type is not None: kwargs[self.sub_cmd.wep_key_type] = wep_key_type
        if bssid is not None: kwargs[self.sub_cmd.bssid] = bssid
        if name is not None: kwargs[self.sub_cmd.name] = name
        if wait is not None: kwargs[self.sub_cmd.wait] = wait
        if private is not None: kwargs[self.sub_cmd.private] = self.sub_cmd.yes if private else self.sub_cmd.no
        if hidden is not None: kwargs[self.sub_cmd.hidden] = self.sub_cmd.yes if private else self.sub_cmd.no
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)
class WiFi_DevHotSpotCommand(ROOT):
    """
       wifi hotspot [ifname ifname] [con-name name] [ssid SSID] [band {a | bg}] [channel channel] [password password]
           Create a Wi-Fi hotspot. The command creates a hotspot connection profile according to Wi-Fi device capabilities and activates it on the device.
           The hotspot is secured with WPA if device/driver supports that, otherwise WEP is used. Use connection down or device disconnect to stop the hotspot.

           Parameters of the hotspot can be influenced by the optional parameters:

           ifname
               what Wi-Fi device is used.

           con-name
               name of the created hotspot connection profile.

           ssid
               SSID of the hotspot.

           band
               Wi-Fi band to use.

           channel
               Wi-Fi channel to use.

           password
               password to use for the created hotspot. If not provided, nmcli will generate a password. The password is either WPA pre-shared key or WEP key.

               Note that --show-secrets global option can be used to print the hotspot password. It is useful especially when the password was generated.
    """
    __cmd__ = 'hotspot'



    class sub_cmd(object):
        ifname = 'ifname'
        ssid = 'ssid'
        wait = '--wait'
        password = 'password'
        con_name = 'con-name'
        band = 'band'
        channel = 'channel'



    def __call__(self, if_name: str = None, con_name: str = None, ssid: str = None, band: str = None, channel: str = None, password: str = None) -> Result:
        """
            show [--active] [id | uuid | path | apath] ID...
                Show details for specified connections. By default, both static configuration and active connection data are displayed.
                When --active option is specified, only the active profiles are taken into account.
                Use global --show-secrets option to display secrets associated with the profile.

                id, uuid, path and apath keywords can be used if ID is ambiguous. Optional ID-specifying keywords are:

                id
                   the ID denotes a connection name.

                uuid
                   the ID denotes a connection UUID.

                path
                   the ID denotes a D-Bus static connection path in the format of /org/freedesktop/NetworkManager/Settings/num or just num.

                apath
                   the ID denotes a D-Bus active connection path in the format of /org/freedesktop/NetworkManager/ActiveConnection/num or just num.

                It is possible to filter the output using the global --fields option. Use the following values:

                profile
                   only shows static profile configuration.

                active
                   only shows active connection data (when the profile is active).

                You can also specify particular fields. For static configuration, use setting and property names as described in nm-settings(5) manual page.
                For active data use GENERAL, IP4, DHCP4, IP6, DHCP6, VPN.

                When no command is given to the nmcli connection, the default action is nmcli connection show.

        :param arg:
        :param id:
        :param uuid:
        :param path:
        :param apath:
        :param active:
        :return:
        """
        args = []
        kwargs = { }
        if if_name is not None: kwargs[self.sub_cmd.ifname] = if_name
        if ssid is not None: kwargs[self.sub_cmd.ssid] = ssid
        if band is not None: kwargs[self.sub_cmd.band] = band
        if channel is not None: kwargs[self.sub_cmd.channel] = channel
        if con_name is not None: kwargs[self.sub_cmd.con_name] = con_name
        if password is not None: kwargs[self.sub_cmd.password] = password
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)
class WiFi_DevRescanCommand(ROOT):
    """
       wifi rescan [ifname ifname] [ssid SSID...]
           Request that NetworkManager immediately re-scan for available access points.
           NetworkManager scans Wi-Fi networks periodically, but in some cases it can be useful to start scanning manually (e.g. after resuming the computer).
           By using ssid, it is possible to scan for a specific SSID, which is useful for APs with hidden
           SSIDs. You can provide multiple ssid parameters in order to scan more SSIDs.

           This command does not show the APs, use nmcli device wifi list for that.
    """
    __cmd__ = 'rescan'



    class sub_cmd(object):
        ifname = 'ifname'
        ssid = 'ssid'



    def __call__(self, if_name: str = None, ssid: str = None) -> Result:
        """
            show [--active] [id | uuid | path | apath] ID...
                Show details for specified connections. By default, both static configuration and active connection data are displayed.
                When --active option is specified, only the active profiles are taken into account.
                Use global --show-secrets option to display secrets associated with the profile.

                id, uuid, path and apath keywords can be used if ID is ambiguous. Optional ID-specifying keywords are:

                id
                   the ID denotes a connection name.

                uuid
                   the ID denotes a connection UUID.

                path
                   the ID denotes a D-Bus static connection path in the format of /org/freedesktop/NetworkManager/Settings/num or just num.

                apath
                   the ID denotes a D-Bus active connection path in the format of /org/freedesktop/NetworkManager/ActiveConnection/num or just num.

                It is possible to filter the output using the global --fields option. Use the following values:

                profile
                   only shows static profile configuration.

                active
                   only shows active connection data (when the profile is active).

                You can also specify particular fields. For static configuration, use setting and property names as described in nm-settings(5) manual page.
                For active data use GENERAL, IP4, DHCP4, IP6, DHCP6, VPN.

                When no command is given to the nmcli connection, the default action is nmcli connection show.

        :param arg:
        :param id:
        :param uuid:
        :param path:
        :param apath:
        :param active:
        :return:
        """
        kwargs = { }
        if if_name is not None: kwargs[self.sub_cmd.ifname] = if_name
        if ssid is not None: kwargs[self.sub_cmd.ssid] = ssid
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)
class WiFiCommands(ROOT):
    """
       wifi [list [ifname ifname] [bssid BSSID]]
           List available Wi-Fi access points. The ifname and bssid options can be used to list APs for a particular interface or with a specific BSSID, respectively.
    """
    __base_command__ = 'device'
    rescan = WiFi_DevRescanCommand(__base_command__)
    hot_spot = WiFi_DevHotSpotCommand(__base_command__)
    connect = WiFi_DevConnectCommand(__base_command__)

class DeviceManager(object):
    """
    DEVICE MANAGEMENT COMMANDS
       nmcli device {status | show | set | connect | reapply | modify | disconnect | delete | monitor | wifi | lldp} [ARGUMENTS...]

       Show and manage network interfaces.
    """
    __base_command__ = 'device'
    def __init__(self):
        self.wifi = WiFiCommands(base=self.__base_command__)
        self.monitor = _DevModifyCommand(base=self.__base_command__)
        self.delete = _DevDeleteCommand(base=self.__base_command__)
        self.disconnect = _DevDisconnectCommand(base=self.__base_command__)
        self.lldp = _Dev_lldp_Command(base=self.__base_command__)
        self.modify = _DevModifyCommand(base=self.__base_command__)
        self.reapply = _DevReapplyCommand(base=self.__base_command__)
        self.connect = _DevConnectCommand(base=self.__base_command__)
        self.set = _DevSetCommand(base=self.__base_command__)
        self.show = _DevShowCommand(base=self.__base_command__)
        self.status = _DevStatusCommand(base=self.__base_command__)

    def __call__(self):
        return self.status()
