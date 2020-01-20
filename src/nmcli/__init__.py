
from .base import ROOT
from .results import Result
from .connection import ConnectionManager
from .device import DeviceManager
from .status import NetworkControlCommand
from .misc import RadioTransmissionControlCommand, MonitorCommand
from .general import GeneralCommand



__all__ = ["nmcli"]


DOCUMENTATION = '''
---
module: nmcli
short_description: Wrapper around nmcli executable itself
description:
    - Execute nmcli command to gather information about network manager
      devices.
'''

# nmcli device wifi connect {SSID} password {password}
class NetworkManagerCLI(ROOT):
    """

    """
    __man_nmcli__ = """

SYNOPSIS
       nmcli [OPTIONS...] {help | general | networking | radio | connection | device | agent | monitor} [COMMAND] [ARGUMENTS...]




DESCRIPTION
       nmcli is a command-line tool for controlling NetworkManager and reporting network status. It can be utilized as a replacement for nm-applet or other graphical clients.  nmcli is used to create, display, edit, delete, activate, and deactivate network connections, as well as control and display network device status.

       Typical uses include:

       ·   Scripts: Utilize NetworkManager via nmcli instead of managing network connections manually.  nmcli supports a terse output format which is better suited for script processing. Note that NetworkManager can also execute scripts, called "dispatcher scripts", in response to network events. See NetworkManager(8) for details
           about these dispatcher scripts.

       ·   Servers, headless machines, and terminals: nmcli can be used to control NetworkManager without a GUI, including creating, editing, starting and stopping network connections and viewing network status.




OPTIONS

       -t | --terse
           Output is terse. This mode is designed and suitable for computer (script) processing.




       -p | --pretty
           Output is pretty. This causes nmcli to produce easily readable outputs for humans, i.e. values are aligned, headers are printed, etc.




       -m | --mode {tabular | multiline}
           Switch between tabular and multiline output:

           tabular
               Output is a table where each line describes a single entry. Columns define particular properties of the entry.

           multiline
               Each entry comprises multiple lines, each property on its own line. The values are prefixed with the property name.

           If omitted, default is tabular for most commands. For the commands producing more structured information, that cannot be displayed on a single line, default is multiline. Currently, they are:

           ·   nmcli connection show ID
           ·   nmcli device show




       -c | --colors {yes | no | auto}
           This option controls color output (using terminal escape sequences).  yes enables colors, no disables them, auto only produces colors when standard output is directed to a terminal. The default value is auto.




       -f | --fields {field1,field2... | all | common}
           This option is used to specify what fields (column names) should be printed. Valid field names differ for specific commands. List available fields by providing an invalid value to the --fields option.  all is used to print all valid field values of the command.  common is used to print common field values of the
           command.

           If omitted, default is common.




       -g | --get-values {field1,field2... | all | common}
           This option is used to print values from specific fields. It is basically a shortcut for --mode tabular --terse --fields and is a convenient way to retrieve values for particular fields. The values are printed one per line without headers.

           If a section is specified instead of a field, the section name will be printed followed by colon separated values of the fields belonging to that section, all on the same line.




       -e | --escape {yes | no}
           Whether to escape : and \ characters in terse tabular mode. The escape character is \.

           If omitted, default is yes.




       -a | --ask
           When using this option nmcli will stop and ask for any missing required arguments, so do not use this option for non-interactive purposes like scripts. This option controls, for example, whether you will be prompted for a password if it is required for connecting to a network.




       -s | --show-secrets
           When using this option nmcli will display passwords and secrets that might be present in an output of an operation. This option also influences echoing passwords typed by user as an input.




       -w | --wait seconds
           This option sets a timeout period for which nmcli will wait for NetworkManager to finish operations. It is especially useful for commands that may take a longer time to complete, e.g. connection activation.

           Specifying a value of 0 instructs nmcli not to wait but to exit immediately with a status of success. The default value depends on the executed command.




       --complete-args
           Instead of conducting the desired action, nmcli will list possible completions for the last argument. This is useful to implement argument completion in shell.

           The exit status will indicate success or return a code 65 to indicate the last argument is a file name.

           NetworkManager ships with command completion support for GNU Bash.




       -v | --version
           Show nmcli version.




       -h | --help
           Print help information.



EXAMPLES
       This section presents various examples of nmcli usage. If you want even more, please refer to nmcli-examples(7) manual page.




       nmcli -t -f RUNNING general
           Tells you whether NetworkManager is running or not.



       nmcli -t -f STATE general
           Shows the overall status of NetworkManager.



       nmcli radio wifi off
           Switches Wi-Fi off.



       nmcli connection show
           Lists all connections NetworkManager has.



       nmcli -p -m multiline -f all con show
           Shows all configured connections in multi-line mode.



       nmcli connection show --active
           Lists all currently active connections.



       nmcli -f name,autoconnect c s
           Shows all connection profile names and their auto-connect property.



       nmcli -p connection show "My default em1"
           Shows details for "My default em1" connection profile.



       nmcli --show-secrets connection show "My Home WiFi"
           Shows details for "My Home WiFi" connection profile with all passwords. Without --show-secrets option, secrets would not be displayed.



       nmcli -f active connection show "My default em1"
           Shows details for "My default em1" active connection, like IP, DHCP information, etc.



       nmcli -f profile con s "My wired connection"
           Shows static configuration details of the connection profile with "My wired connection" name.



       nmcli -p con up "My wired connection" ifname eth0
           Activates the connection profile with name "My wired connection" on interface eth0.
           The -p option makes nmcli show progress of the activation.



       nmcli con up 6b028a27-6dc9-4411-9886-e9ad1dd43761 ap 00:3A:98:7C:42:D3
           connects the Wi-Fi connection with UUID 6b028a27-6dc9-4411-9886-e9ad1dd43761 to the AP with BSSID 00:3A:98:7C:42:D3.



       nmcli device status
           shows the status for all devices.



       nmcli dev disconnect em2
           Disconnects a connection on interface em2 and marks the device as unavailable for auto-connecting.
           As a result, no connection will automatically be activated on the device until the device's 'autoconnect' is set to TRUE or the user manually activates a connection.



       nmcli -f GENERAL,WIFI-PROPERTIES dev show wlan0
           Shows details for wlan0 interface; only GENERAL and WIFI-PROPERTIES sections will be shown.



       nmcli -f CONNECTIONS device show wlp3s0
           Shows all available connection profiles for your Wi-Fi interface wlp3s0.



       nmcli dev wifi
           Lists available Wi-Fi access points known to NetworkManager.



       nmcli dev wifi con "Cafe Hotspot 1" password caffeine name "My cafe"
           Creates a new connection named "My cafe" and then connects it to "Cafe Hotspot 1" SSID using password "caffeine".
           This is mainly useful when connecting to "Cafe Hotspot 1" for the first time.
           Next time, it is better to use nmcli con up id "My cafe" so that the existing connection profile can be used and no additional is created.



       nmcli -s dev wifi hotspot con-name QuickHotspot
           Creates a hotspot profile and connects it. Prints the hotspot password the user should use to connect to the hotspot from other devices.



       nmcli dev modify em1 ipv4.method shared
           Starts IPv4 connection sharing using em1 device. The sharing will be active until the device is disconnected.



       nmcli dev modify em1 ipv6.address 2001:db8::a:bad:c0de
           Temporarily adds an IP address to a device. The address will be removed when the same connection is activated again.



       nmcli connection add type ethernet autoconnect no ifname eth0
           Non-interactively adds an Ethernet connection tied to eth0 interface with automatic IP configuration (DHCP), and disables the connection's autoconnect flag.



       nmcli c a ifname Maxipes-fik type vlan dev eth0 id 55
           Non-interactively adds a VLAN connection with ID 55. The connection will use eth0 and the VLAN interface will be named Maxipes-fik.



       nmcli c a ifname eth0 type ethernet ipv4.method disabled ipv6.method link-local
           Non-interactively adds a connection that will use eth0 Ethernet interface and only have an IPv6 link-local address configured.



       nmcli connection edit ethernet-em1-2
           Edits existing "ethernet-em1-2" connection in the interactive editor.



       nmcli connection edit type ethernet con-name "yet another Ethernet connection"
           Adds a new Ethernet connection in the interactive editor.



       nmcli con mod ethernet-2 connection.autoconnect no
           Modifies 'autoconnect' property in the 'connection' setting of 'ethernet-2' connection.




       nmcli con mod "Home Wi-Fi" wifi.mtu 1350
           Modifies 'mtu' property in the 'wifi' setting of 'Home Wi-Fi' connection.



       nmcli con mod em1-1 ipv4.method manual ipv4.addr "192.168.1.23/24 192.168.1.1, 10.10.1.5/8, 10.0.0.11"
           Sets manual addressing and the addresses in em1-1 profile.



       nmcli con modify ABC +ipv4.dns 8.8.8.8
           Appends a Google public DNS server to DNS servers in ABC profile.



       nmcli con modify ABC -ipv4.addresses "192.168.100.25/24 192.168.1.1"
           Removes the specified IP address from (static) profile ABC.



       nmcli con import type openvpn file ~/Downloads/frootvpn.ovpn
           Imports an OpenVPN configuration to NetworkManager.



       nmcli con export corp-vpnc /home/joe/corpvpn.conf
           Exports NetworkManager VPN profile corp-vpnc as standard Cisco (vpnc) configuration.
    """

    connections = ConnectionManager()
    devices = DeviceManager()
    general = GeneralCommand()
    rtc = RadioTransmissionControlCommand()
    monitor = MonitorCommand()
    state = NetworkControlCommand()

    def Status(self) -> Result:
        return self.state.connectivity()

    def help(self) -> str:
        return ''

    def __init__(self):
        pass

nmcli = NetworkManagerCLI()

