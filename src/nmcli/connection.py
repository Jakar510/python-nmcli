
from .base import ROOT
from .results import Result


___all__ = ['ConnectionCommand']






class _ConnShowCommand(ROOT):
    """
       show [--active] [--order [+-]category:...]
           List in-memory and on-disk connection profiles, some of which may also be active if a device is using that connection profile.
           Without a parameter, all profiles are listed. When --active option is specified, only the active profiles are shown.

           The --order option can be used to get custom ordering of connections.
           The connections can be ordered by active status (active), name (name), type (type) or D-Bus path (path).
           If connections are equal according to a sort order category, an additional category can be specified. The default sorting order is equivalent to
           --order active:name:path.  + or no prefix means sorting in ascending order (alphabetically or in numbers), - means reverse (descending) order.
           The category names can be abbreviated (e.g.  --order -a:na).


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
    """
    __cmd__ = 'show'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        apath = 'apath'
        active = '--active'
        order = '--order'
    def __call__(self, arg: str, *, id: bool = None, uuid: bool = None, path: str = None, apath: str = None, active: bool = None) -> Result:
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
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = arg
        if uuid is not None: kwargs[self.sub_cmd.uuid] = arg
        if path is not None: kwargs[self.sub_cmd.path] = arg
        if apath is not None: kwargs[self.sub_cmd.apath] = arg
        if active is not None: args.append(self.sub_cmd.active)
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

    def order(self, active: bool, *args, **kwargs):
        """
       show [--active] [--order [+-]category:...]
           List in-memory and on-disk connection profiles, some of which may also be active if a device is using that connection profile.
           Without a parameter, all profiles are listed.
           When --active option is specified, only the active profiles are shown.

           The --order option can be used to get custom ordering of connections.
           The connections can be ordered by active status (active), name (name), type (type) or D-Bus path (path).
           If connections are equal according to a sort order category, an additional category can be specified. The default sorting order is equivalent to
           --order active:name:path.  + or no prefix means sorting in ascending order (alphabetically or in numbers), - means reverse (descending) order.
           The category names can be abbreviated (e.g.  --order -a:na).

        :param active:
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

class _ConnUpCommand(ROOT):
    """
       up [id | uuid | path] ID [ifname ifname] [ap BSSID] [passwd-file file]
           Activate a connection. The connection is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid or path can be used. When requiring a particular device to activate the connection on, the ifname option with interface name should be given. If the ID is not given an ifname is required, and
           NetworkManager will activate the best available connection for the given ifname. In case of a VPN connection, the ifname option specifies the device of the base connection. The ap option specify what particular AP should be used in case of a Wi-Fi connection.

           If --wait option is not specified, the default timeout will be 90 seconds.

           See connection show above for the description of the ID-specifying keywords.

           Available options are:

           ifname
               interface that will be used for activation.

           ap
               BSSID of the AP which the command should connect to (for Wi-Fi connections).

           passwd-file
               some networks may require credentials during activation. You can give these credentials using this option. Each line of the file should contain one password in the form:

                   setting_name.property_name:the password

               For example, for WPA Wi-Fi with PSK, the line would be

                   802-11-wireless-security.psk:secret12345

               For 802.1X password, the line would be

                   802-1x.password:my 1X password

               nmcli also accepts wifi-sec and wifi strings instead of 802-11-wireless-security. When NetworkManager requires a password and it is not given, nmcli will ask for it when run with --ask. If --ask was not passed, NetworkManager can ask another secret agent that may be running (typically a GUI secret agent, such as
               nm-applet or gnome-shell).

    """
    __cmd__ = 'up'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        apath = 'apath'
        ifname = 'ifname'
        ap = 'ap'
        passwd_file = 'passwd-file'
    def __call__(self, arg: str, *, id: bool = None, uuid: bool = None, path: bool = None, if_name: str = None, ap: str = None, passwd_file: str = None) -> Result:
        """
            up [id | uuid | path] ID [ifname ifname] [ap BSSID] [passwd-file file]

        :param arg:
        :param id:
        :param uuid:
        :param path:
        :param ifname:
        :param ap:
        :param passwd_file:
        :return:
        """
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = arg
        if uuid is not None: kwargs[self.sub_cmd.uuid] = arg
        if if_name is not None: kwargs[self.sub_cmd.ifname] = if_name
        if ap is not None: kwargs[self.sub_cmd.ap] = ap
        if passwd_file is not None: kwargs[self.sub_cmd.passwd_file] = passwd_file
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnDownCommand(ROOT):
    """
       down [id | uuid | path | apath] ID...
           Deactivate a connection from a device without preventing the device from further auto-activation. Multiple connections can be passed to the command.

           Be aware that this command deactivates the specified active connection, but the device on which the connection was active, is still ready to connect and will perform auto-activation by looking for a suitable connection that has the 'autoconnect' flag set. This includes the just deactivated connection. So if the
           connection is set to auto-connect, it will be automatically started on the disconnected device again.

           In most cases you may want to use device disconnect command instead.

           The connection is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid, path or apath can be used.

           See connection show above for the description of the ID-specifying keywords.

           If --wait option is not specified, the default timeout will be 10 seconds.
    """
    __cmd__ = 'down'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        apath = 'apath'
    def __call__(self, arg: str, *, id: bool = None, uuid: bool = None, path: bool = None, apath: bool = None) -> Result:
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = arg
        if uuid is not None: kwargs[self.sub_cmd.uuid] = arg
        if path is not None: kwargs[self.sub_cmd.path] = arg
        if apath is not None: kwargs[self.sub_cmd.apath] = arg
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnModifyCommand(ROOT):
    """
       modify [--temporary] [id | uuid | path] ID {option value | [+|-]setting.property value}...
           Add, modify or remove properties in the connection profile.

           To set the property just specify the property name followed by the value. An empty value ("") removes the property value.

           In addition to the properties, you can also use short names for some of the properties. Consult the PROPERTY ALIASES section for details.

           If you want to append an item to the existing value, use + prefix for the property name. If you want to remove just one item from container-type property, use - prefix for the property name and specify a value or an zero-based index of the item to remove (or option name for properties with named options) as value. The +
           and - modifies only have a real effect for multi-value (container) properties like ipv4.dns, ipv4.addresses, bond.options, etc.

           See nm-settings(5) for complete reference of setting and property names, their descriptions and default values. The setting and property can be abbreviated provided they are unique.

           The connection is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid or path can be used.
    """
    __cmd__ = 'modify'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        option = 'option'
        temporary = '--temporary'
    def __call__(self, arg: str, *args, temporary: bool = None, id: bool = None, uuid: bool = None, path: bool = None, option: bool = None, **kwargs) -> Result:
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = arg
        if uuid is not None: kwargs[self.sub_cmd.uuid] = arg
        if path is not None: kwargs[self.sub_cmd.path] = arg

        if option is not None: kwargs[self.sub_cmd.option] = option
        if temporary is True: args.append(self.sub_cmd.temporary)
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnAddCommand(ROOT):
    """
       add [save {yes | no}] {option value | [+|-]setting.property value}...
           Create a new connection using specified properties.

           You need to describe the newly created connections with the property and value pairs. See nm-settings(5) for the complete reference. You can also use the aliases described in PROPERTY ALIASES section. The syntax is the same as of the nmcli connection modify command.

           To construct a meaningful connection you at the very least need to set the connection.type property (or use the type alias) to one of known NetworkManager connection types:

           ·   ethernet
           ·   wifi
           ·   wimax
           ·   pppoe
           ·   gsm
           ·   cdma
           ·   infiniband
           ·   bluetooth
           ·   vlan
           ·   bond
           ·   bond-slave
           ·   team
           ·   team-slave
           ·   bridge
           ·   bridge-slave
           ·   vpn
           ·   olpc-mesh
           ·   adsl
           ·   tun
           ·   ip-tunnel
           ·   macvlan
           ·   vxlan
           ·   dummy


           The most typical uses are described in the EXAMPLES section.

           Aside from the properties and values two special options are accepted:

           save
               Controls whether the connection should be persistent, i.e. NetworkManager should store it on disk (default: yes).

           --
               If a single -- argument is encountered it is ignored. This is for compatibility with older versions on nmcli.
    """
    __cmd__ = 'add'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'

        save = 'save'
        yes = 'yes'
        no = 'no'
        temporary = '--temporary'

        ethernet = "ethernet"
        wifi = "wifi"
        wimax = "wimax"
        pppoe = "pppoe"
        gsm = "gsm"
        cdma = "cdma"
        infiniband = "infiniband"
        bluetooth = "bluetooth"
        vlan = "vlan"
        bond = "bond"
        bond_slave = "bond-slave"
        team = "team"
        team_slave = "team-slave"
        bridge = "bridge"
        bridge_slave = "bridge-slave"
        vpn = "vpn"
        olpc_mesh = "olpc-mesh"
        adsl = "adsl"
        tun = "tun"
        ip_tunnel = "ip-tunnel"
        macvlan = "macvlan"
        vxlan = "vxlan"
        dummy = "dummy"
    def __call__(self, ID: str, *args, id: bool = None, uuid: bool = None, save: bool = True, temporary: bool = True, **kwargs) -> Result:
        args = []
        if save is not None: kwargs[self.sub_cmd.save] = self.sub_cmd.yes if save else self.sub_cmd.no
        if temporary is True: args.append(self.sub_cmd.temporary)
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnEditCommand(ROOT):
    """
       edit {[id | uuid | path] ID | [type type] [con-name name] }
           Edit an existing connection or add a new one, using an interactive editor.

           The existing connection is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid, or path can be used. See connection show above for the description of the ID-specifying keywords. Not providing an ID means that a new connection will be added.

           The interactive editor will guide you through the connection editing and allow you to change connection parameters according to your needs by means of a simple menu-driven interface. The editor indicates what settings and properties can be modified and provides in-line help.

           Available options:

           type
               type of the new connection; valid types are the same as for connection add command.

           con-name
               name for the new connection. It can be changed later in the editor.

           See also nm-settings(5) for all NetworkManager settings and property names, and their descriptions; and nmcli-examples(7) for sample editor sessions.
    """
    __cmd__ = 'clone'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        type = 'type'
        con_name = 'con-name'
        temporary = 'temporary'
    def ID(self, arg: str, *, id: bool = None, uuid: bool = None, path: bool = None) -> Result:
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = arg
        if uuid is not None: kwargs[self.sub_cmd.uuid] = arg
        if path is not None: kwargs[self.sub_cmd.path] = arg
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

    def __call__(self, type: str, con_name: str):
        kwargs = {}
        if type is not None: kwargs[self.sub_cmd.type] = type
        if con_name is not None: kwargs[self.sub_cmd.con_name] = con_name
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _ConnCloneCommand(ROOT):
    """
       clone [--temporary] [id | uuid | path] ID new_name
           Clone a connection. The connection to be cloned is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid or path can be used. See connection show above for the description of the ID-specifying keywords.  new_name is the name of the new cloned connection. The new connection will be the exact
           copy except the connection.id (new_name) and connection.uuid (generated) properties.

           The new connection profile will be saved as persistent unless --temporary option is specified, in which case the new profile won't exist after NetworkManager restart.
    """
    __cmd__ = 'clone'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
        type = 'type'
        temporary = 'temporary'
    def __call__(self, ID: str, new_name: str, *, id: bool = None, uuid: bool = None, path: bool = None, temporary: bool = None) -> Result:
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = ID
        if uuid is not None: kwargs[self.sub_cmd.uuid] = ID
        if path is not None: kwargs[self.sub_cmd.path] = ID
        args.append(new_name)

        if temporary is True: args.append(self.sub_cmd.temporary)
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnDeleteCommand(ROOT):
    """
       delete [id | uuid | path] ID...
           Delete a configured connection. The connection to be deleted is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid or path can be used. See connection show above for the description of the ID-specifying keywords.

           If --wait option is not specified, the default timeout will be 10 seconds.
    """
    __cmd__ = 'delete'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
    def __call__(self, ID: str, *, id: bool = None, uuid: bool = None, path: bool = None) -> Result:
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = ID
        if uuid is not None: kwargs[self.sub_cmd.uuid] = ID
        if path is not None: kwargs[self.sub_cmd.path] = ID
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _ConnMonitorCommand(ROOT):
    """
       monitor [id | uuid | path] ID...
           Monitor connection profile activity. This command prints a line whenever the specified connection changes. The connection to be monitored is identified by its name, UUID or D-Bus path. If ID is ambiguous, a keyword id, uuid or path can be used. See connection show above for the description of the ID-specifying keywords.

           Monitors all connection profiles in case none is specified. The command terminates when all monitored connections disappear. If you want to monitor connection creation consider using the global monitor with nmcli monitor command.
    """
    __cmd__ = 'monitor'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
    def __call__(self, ID: str, *, id: bool = None, uuid: bool = None, path: bool = None) -> Result:
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = ID
        if uuid is not None: kwargs[self.sub_cmd.uuid] = ID
        if path is not None: kwargs[self.sub_cmd.path] = ID
        return self._run_action(self.__base_command__, self.__cmd__, kwargs=kwargs)

class _ConnReloadCommand(ROOT):
    """
       reload
           Reload all connection files from disk.
           NetworkManager does not monitor changes to connection files by default.
           So you need to use this command in order to tell NetworkManager to re-read the connection profiles from disk when a change was made to them.
           However, the auto-loading feature can be enabled and then NetworkManager will reload connection files any time they change (monitor-connection-files=true in NetworkManager.conf(5)).
    """
    __cmd__ = 'reload'
    def __call__(self):
        return self._run_action(self.__base_command__, self.__cmd__)

class _ConnLoadCommand(ROOT):
    """
       load filename...
           Load/reload one or more connection files from disk. Use this after manually editing a connection file to ensure that NetworkManager is aware of its latest state.
    """
    __cmd__ = 'load'
    def __call__(self, file_name: str = None) -> Result:
        return self._run_action(self.__base_command__, self.__cmd__, file_name)

class _ConnImportCommand(ROOT):
    """
       import [--temporary] type type file file
           Import an external/foreign configuration as a NetworkManager connection profile. The type of the input file is specified by type option.

           Only VPN configurations are supported at the moment. The configuration is imported by NetworkManager VPN plugins.  type values are the same as for vpn-type option in nmcli connection add. VPN configurations are imported by VPN plugins. Therefore the proper VPN plugin has to be installed so that nmcli could import the
           data.

           The imported connection profile will be saved as persistent unless --temporary option is specified, in which case the new profile won't exist after NetworkManager restart.
    """
    __cmd__ = 'import'
    class sub_cmd(object):
        type = 'type'
        file = 'file'
        temporary = '--temporary'
    # noinspection PyShadowingBuiltins
    def __call__(self, type: str, file: str, *, temporary: bool = None) -> Result:
        args = []
        kwargs = {}
        if type is not None: kwargs[self.sub_cmd.type] = type
        if file is not None: kwargs[self.sub_cmd.file] = file
        if temporary is True: args.append(self.sub_cmd.temporary)
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)

class _ConnExportCommand(ROOT):
    """
       export [id | uuid | path] ID [file]
           Export a connection.

           Only VPN connections are supported at the moment. A proper VPN plugin has to be installed so that nmcli could export a connection. If no file is provided, the VPN configuration data will be printed to standard output.
    """
    __cmd__ = 'export'
    class sub_cmd(object):
        ID = 'id'
        uuid = 'uuid'
        path = 'path'
    def __call__(self, ID: str, *, id: bool = None, uuid: bool = None, path: bool = None, file: str = None) -> Result:
        args = []
        kwargs = {}
        if id is not None: kwargs[self.sub_cmd.ID] = ID
        if uuid is not None: kwargs[self.sub_cmd.uuid] = ID
        if path is not None: kwargs[self.sub_cmd.path] = ID
        if file is not None: kwargs[''] = file
        return self._run_action(self.__base_command__, self.__cmd__, args=args, kwargs=kwargs)



class ConnectionManager(object):
    """
    nmcli connection {show | up | down | modify | add | edit | clone | delete | monitor | reload | load | import | export} [ARGUMENTS...]

       NetworkManager stores all network configuration as "connections", which are collections of data (Layer2 details, IP addressing, etc.) that describe how to create or connect to a network. A connection is "active" when a device uses that connection's configuration to create or connect to a network. There may be multiple
       connections that apply to a device, but only one of them can be active on that device at any given time. The additional connections can be used to allow quick switching between different networks and configurations.

       Consider a machine which is usually connected to a DHCP-enabled network, but sometimes connected to a testing network which uses static IP addressing. Instead of manually reconfiguring eth0 each time the network is changed, the settings can be saved as two connections which both apply to eth0, one for DHCP (called default)
       and one with the static addressing details (called testing). When connected to the DHCP-enabled network the user would run nmcli con up default , and when connected to the static network the user would run nmcli con up testing.

    """
    __base_command__: str = 'con'
    def __init__(self):
        self.Show = _ConnShowCommand(base=self.__base_command__)
        self.Up = _ConnUpCommand(base=self.__base_command__)
        self.Down = _ConnDownCommand(base=self.__base_command__)
        self.Modify = _ConnModifyCommand(base=self.__base_command__)
        self.Add = _ConnAddCommand(base=self.__base_command__)
        self.Edit = _ConnEditCommand(base=self.__base_command__)
        self.Clone = _ConnEditCommand(base=self.__base_command__)
        self.Delete = _ConnDeleteCommand(base=self.__base_command__)
        self.Monitor = _ConnMonitorCommand(base=self.__base_command__)
        self.Reload = _ConnReloadCommand(base=self.__base_command__)
        self.Load = _ConnLoadCommand(base=self.__base_command__)
        self.Import = _ConnImportCommand(base=self.__base_command__)
        self.Export = _ConnExportCommand(base=self.__base_command__)

