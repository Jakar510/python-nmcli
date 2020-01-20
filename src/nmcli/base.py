import re
import shlex
import subprocess
from .results import Result
from .constants import NMCLI_FIELDS



___all__ = ['ROOT', 'error_codes', 'Exit_Status', 'Result']




class Exit_Status(object):
    """
EXIT STATUS
       nmcli exits with status 0 if it succeeds, a value greater than 0 is returned if an error occurs.

       0
           Success – indicates the operation succeeded.

       1
           Unknown or unspecified error.

       2
           Invalid user input, wrong nmcli invocation.

       3
           Timeout expired (see --wait option).

       4
           Connection activation failed.

       5
           Connection deactivation failed.

       6
           Disconnecting device failed.

       7
           Connection deletion failed.

       8
           NetworkManager is not running.

       10
           Connection, device, or access point does not exist.

       65
           When used with --complete-args option, a file name is expected to follow.
    """
    status = {
                0: 'Success – indicates the operation succeeded.',
                1: 'Unknown or unspecified error.',
                2: 'Invalid user input, wrong nmcli invocation.',
                3: 'Timeout expired (see --wait option).',
                4: 'Connection activation failed.',
                5: 'Connection deactivation failed.',
                6: 'Disconnecting device failed.',
                7: 'Connection deletion failed.',
                8: 'NetworkManager is not running.',
                10: 'Connection, device, or access point does not exist.',
                65: 'When used with --complete-args option, a file name is expected to follow.',
            }
    def __call__(self, code: int) -> str:
        if code in self.status: return self.status[code]
        else: return f'code: {code}  |   {self.status[1]}'
    @staticmethod
    def IsOk(code: int):
        return code == 0
error_codes = Exit_Status()


class Tables(object):
    """
    PROPERTY ALIASES
       Apart from the property-value pairs, connection add, connection modify and device modify also accept short forms of some properties.
       They exist for convenience.
       Some aliases can affect multiple connection properties at once.

       The overview of the aliases is below.
       An actual connection type is used to disambiguate these options from the options of the same name that are valid for multiple connection types (such as mtu).



       Table 1. Options for all connections
       ┌────────────┬───────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────┐
       │Alias       │ Property                  │ Note                                                                                │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │type        │ connection.type           │ This alias also accepts values of bond-slave, team-slave and bridge-slave. They     │
       │            │                           │ create ethernet connection profiles. Their use is discouraged in favor of using a   │
       │            │                           │ specific type with master option.                                                   │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │con-name    │ connection.id             │ When not provided a default name is generated: <type>[-<ifname>][-<num>]).          │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │autoconnect │ connection.autoconnect    │                                                                                     │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │ifname      │ connection.interface-name │ A value of * will be interpreted as no value, making the connection profile         │
       │            │                           │ interface-independent.  Note: use quotes around * to suppress shell expansion.  For │
       │            │                           │ bond, team and bridge connections a default name will be generated if not set.      │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │master      │ connection.master         │ Value specified here will be canonicalized.  It can be prefixed with ifname/, uuid/ │
       │            │                           │ or id/ to disambiguate it.                                                          │
       ├────────────┼───────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │slave-type  │ connection.slave-type     │                                                                                     │
       └────────────┴───────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘

       Table 2. PPPoE options
       ┌─────────┬────────────────┐
       │Alias    │ Property       │
       ├─────────┼────────────────┤
       │username │ pppoe.username │
       ├─────────┼────────────────┤
       │password │ pppoe.password │
       ├─────────┼────────────────┤
       │service  │ pppoe.service  │
       ├─────────┼────────────────┤
       │parent   │ pppoe.parent   │
       └─────────┴────────────────┘

       Table 3. Wired Ethernet options
       ┌───────────┬──────────────────────────┐
       │Alias      │ Property                 │
       ├───────────┼──────────────────────────┤
       │mtu        │ wired.mtu                │
       ├───────────┼──────────────────────────┤
       │mac        │ wired.mac-address        │
       ├───────────┼──────────────────────────┤
       │cloned-mac │ wired.cloned-mac-address │
       └───────────┴──────────────────────────┘

       Table 4. Infiniband options
       ┌───────────────┬───────────────────────────┐
       │Alias          │ Property                  │
       ├───────────────┼───────────────────────────┤
       │mtu            │ infiniband.mtu            │
       ├───────────────┼───────────────────────────┤
       │mac            │ infiniband.mac-address    │
       ├───────────────┼───────────────────────────┤
       │transport-mode │ infiniband.transport-mode │
       ├───────────────┼───────────────────────────┤
       │parent         │ infiniband.parent         │
       ├───────────────┼───────────────────────────┤
       │p-key          │ infiniband.p-key          │
       └───────────────┴───────────────────────────┘

       Table 5. Wi-Fi options
       ┌───────────┬─────────────────────────────┐
       │Alias      │ Property                    │
       ├───────────┼─────────────────────────────┤
       │ssid       │ wireless.ssid               │
       ├───────────┼─────────────────────────────┤
       │mode       │ wireless.mode               │
       ├───────────┼─────────────────────────────┤
       │mtu        │ wireless.mtu                │
       ├───────────┼─────────────────────────────┤
       │mac        │ wireless.mac-address        │
       ├───────────┼─────────────────────────────┤
       │cloned-mac │ wireless.cloned-mac-address │
       └───────────┴─────────────────────────────┘

       Table 6. WiMax options
       ┌──────┬────────────────────┐
       │Alias │ Property           │
       ├──────┼────────────────────┤
       │nsp   │ wimax.network-name │
       ├──────┼────────────────────┤
       │mac   │ wimax.mac-address  │
       └──────┴────────────────────┘

       Table 7. GSM options
       ┌─────────┬──────────────┐
       │Alias    │ Property     │
       ├─────────┼──────────────┤
       │apn      │ gsm.apn      │
       ├─────────┼──────────────┤
       │user     │ gsm.username │
       ├─────────┼──────────────┤
       │password │ gsm.password │
       └─────────┴──────────────┘

       Table 8. CDMA options
       ┌─────────┬───────────────┐
       │Alias    │ Property      │
       ├─────────┼───────────────┤
       │user     │ cdma.username │
       ├─────────┼───────────────┤
       │password │ cdma.password │
       └─────────┴───────────────┘

       Table 9. Bluetooth options
       ┌────────┬──────────────────┬─────────────────────────────────────────────────────────────────────────────────────┐
       │Alias   │ Property         │ Note                                                                                │
       ├────────┼──────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │addr    │ bluetooth.bdaddr │                                                                                     │
       ├────────┼──────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │bt-type │ bluetooth.type   │ Apart from the usual panu, nap and dun options, the values of dun-gsm and dun-cdma  │
       │        │                  │ can be used for compatibility with older versions. They are equivalent to using dun │
       │        │                  │ and setting appropriate gsm.* or cdma.* properties.                                 │
       └────────┴──────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘

       Table 10. VLAN options
       ┌────────┬───────────────────────────┐
       │Alias   │ Property                  │
       ├────────┼───────────────────────────┤
       │dev     │ vlan.parent               │
       ├────────┼───────────────────────────┤
       │id      │ vlan.id                   │
       ├────────┼───────────────────────────┤
       │flags   │ vlan.flags                │
       ├────────┼───────────────────────────┤
       │ingress │ vlan.ingress-priority-map │
       ├────────┼───────────────────────────┤
       │egress  │ vlan.egress-priority-map  │
       └────────┴───────────────────────────┘

       Table 11. Bonding options
       ┌──────────────┬──────────────┬─────────────────────────────────────────────────────────────────────────────────────┐
       │Alias         │ Property     │ Note                                                                                │
       ├──────────────┼──────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │mode          │              │ Setting each of these adds the option to bond.options property.  It's equivalent to │
       ├──────────────┤              │ the +bond.options 'option=value' syntax.                                            │
       │primary       │              │                                                                                     │
       ├──────────────┤              │                                                                                     │
       │miimon        │              │                                                                                     │
       ├──────────────┤              │                                                                                     │
       │downdelay     │              │                                                                                     │
       ├──────────────┤ bond.options │                                                                                     │
       │updelay       │              │                                                                                     │
       ├──────────────┤              │                                                                                     │
       │arp-interval  │              │                                                                                     │
       ├──────────────┤              │                                                                                     │
       │arp-ip-target │              │                                                                                     │
       ├──────────────┤              │                                                                                     │
       │lacp-rate     │              │                                                                                     │
       └──────────────┴──────────────┴─────────────────────────────────────────────────────────────────────────────────────┘

       Table 12. Team options
       ┌───────┬─────────────┬─────────────────────────────────────────────────────────────────────────────────┐
       │Alias  │ Property    │ Note                                                                            │
       ├───────┼─────────────┼─────────────────────────────────────────────────────────────────────────────────┤
       │config │ team.config │ Either a filename or a team configuration in JSON format. To enforce one or the │
       │       │             │ other, the value can be prefixed with "file://" or "json://".                   │
       └───────┴─────────────┴─────────────────────────────────────────────────────────────────────────────────┘

       Table 13. Team port options
       ┌───────┬──────────────────┬─────────────────────────────────────────────────────────────────────────────────┐
       │Alias  │ Property         │ Note                                                                            │
       ├───────┼──────────────────┼─────────────────────────────────────────────────────────────────────────────────┤
       │config │ team-port.config │ Either a filename or a team configuration in JSON format. To enforce one or the │
       │       │                  │ other, the value can be prefixed with "file://" or "json://".                   │
       └───────┴──────────────────┴─────────────────────────────────────────────────────────────────────────────────┘

       Table 14. Bridge options
       ┌───────────────────┬───────────────────────────┐
       │Alias              │ Property                  │
       ├───────────────────┼───────────────────────────┤
       │stp                │ bridge.stp                │
       ├───────────────────┼───────────────────────────┤
       │priority           │ bridge.priority           │
       ├───────────────────┼───────────────────────────┤
       │forward-delay      │ bridge.forward-delay      │
       ├───────────────────┼───────────────────────────┤
       │hello-time         │ bridge.hello-time         │
       ├───────────────────┼───────────────────────────┤
       │max-age            │ bridge.max-age            │
       ├───────────────────┼───────────────────────────┤
       │ageing-time        │ bridge.ageing-time        │
       ├───────────────────┼───────────────────────────┤
       │group-forward-mask │ bridge.group-forward-mask │
       ├───────────────────┼───────────────────────────┤
       │multicast-snooping │ bridge.multicast-snooping │
       ├───────────────────┼───────────────────────────┤
       │mac                │ bridge.mac-address        │
       ├───────────────────┼───────────────────────────┤
       │priority           │ bridge-port.priority      │
       ├───────────────────┼───────────────────────────┤
       │path-cost          │ bridge-port.path-cost     │
       ├───────────────────┼───────────────────────────┤
       │hairpin            │ bridge-port.hairpin-mode  │
       └───────────────────┴───────────────────────────┘

       Table 15. VPN options
       ┌─────────┬──────────────────┐
       │Alias    │ Property         │
       ├─────────┼──────────────────┤
       │vpn-type │ vpn.service-type │
       ├─────────┼──────────────────┤
       │user     │ vpn.user-name    │
       └─────────┴──────────────────┘

       Table 16. OLPC Mesh options
       ┌─────────────┬────────────────────────────────┐
       │Alias        │ Property                       │
       ├─────────────┼────────────────────────────────┤
       │ssid         │ olpc-mesh.ssid                 │
       ├─────────────┼────────────────────────────────┤
       │channel      │ olpc-mesh.channel              │
       ├─────────────┼────────────────────────────────┤
       │dhcp-anycast │ olpc-mesh.dhcp-anycast-address │
       └─────────────┴────────────────────────────────┘

       Table 17. ADSL options
       ┌──────────────┬────────────────────┐
       │Alias         │ Property           │
       ├──────────────┼────────────────────┤
       │username      │ adsl.username      │
       ├──────────────┼────────────────────┤
       │protocol      │ adsl.protocol      │
       ├──────────────┼────────────────────┤
       │password      │ adsl.password      │
       ├──────────────┼────────────────────┤
       │encapsulation │ adsl.encapsulation │
       └──────────────┴────────────────────┘

       Table 18. MACVLAN options
       ┌──────┬────────────────┐
       │Alias │ Property       │
       ├──────┼────────────────┤
       │dev   │ macvlan.parent │
       ├──────┼────────────────┤
       │mode  │ macvlan.mode   │
       ├──────┼────────────────┤
       │tap   │ macvlan.tap    │
       └──────┴────────────────┘

       Table 19. MACsec options
       ┌────────┬────────────────┐
       │Alias   │ Property       │
       ├────────┼────────────────┤
       │dev     │ macsec.parent  │
       ├────────┼────────────────┤
       │mode    │ macsec.mode    │
       ├────────┼────────────────┤
       │encrypt │ macsec.encrypt │
       ├────────┼────────────────┤
       │cak     │ macsec.cak     │
       ├────────┼────────────────┤
       │ckn     │ macsec.ckn     │
       ├────────┼────────────────┤
       │port    │ macsec.port    │
       └────────┴────────────────┘

       Table 20. VxLAN options
       ┌─────────────────┬────────────────────────┐
       │Alias            │ Property               │
       ├─────────────────┼────────────────────────┤
       │id               │ vxlan.id               │
       ├─────────────────┼────────────────────────┤
       │remote           │ vxlan.remote           │
       ├─────────────────┼────────────────────────┤
       │dev              │ vxlan.parent           │
       ├─────────────────┼────────────────────────┤
       │local            │ vxlan.local            │
       ├─────────────────┼────────────────────────┤
       │source-port-min  │ vxlan.source-port-min  │
       ├─────────────────┼────────────────────────┤
       │source-port-max  │ vxlan.source-port-max  │
       ├─────────────────┼────────────────────────┤
       │destination-port │ vxlan.destination-port │
       └─────────────────┴────────────────────────┘

       Table 21. Tun options
       ┌────────────┬─────────────────┐
       │Alias       │ Property        │
       ├────────────┼─────────────────┤
       │mode        │ tun.mode        │
       ├────────────┼─────────────────┤
       │owner       │ tun.owner       │
       ├────────────┼─────────────────┤
       │group       │ tun.group       │
       ├────────────┼─────────────────┤
       │pi          │ tun.pi          │
       ├────────────┼─────────────────┤
       │vnet-hdr    │ tun.vnet-hdr    │
       ├────────────┼─────────────────┤
       │multi-queue │ tun.multi-queue │
       └────────────┴─────────────────┘

       Table 22. IP tunneling options
       ┌───────┬──────────────────┐
       │Alias  │ Property         │
       ├───────┼──────────────────┤
       │mode   │ ip-tunnel.mode   │
       ├───────┼──────────────────┤
       │local  │ ip-tunnel.local  │
       ├───────┼──────────────────┤
       │remote │ ip-tunnel.remote │
       ├───────┼──────────────────┤
       │dev    │ ip-tunnel.parent │
       └───────┴──────────────────┘

       Table 23. IPv4 options
       ┌──────┬────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────┐
       │Alias │ Property                   │ Note                                                                               │
       ├──────┼────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┤
       │ip4   │ ipv4.addresses ipv4.method │ The alias is equivalent to the +ipv4.addresses syntax and also sets ipv4.method to │
       │      │                            │ manual. It can be specified multiple times.                                        │
       ├──────┼────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┤
       │gw4   │ ipv4.gateway               │                                                                                    │
       └──────┴────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────┘

       Table 24. IPv6 options
       ┌──────┬────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────┐
       │Alias │ Property                   │ Note                                                                               │
       ├──────┼────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┤
       │ip6   │ ipv6.addresses ipv6.method │ The alias is equivalent to the +ipv6.addresses syntax and also sets ipv6.method to │
       │      │                            │ manual. It can be specified multiple times.                                        │
       ├──────┼────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┤
       │gw6   │ ipv6.gateway               │                                                                                    │
       └──────┴────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────┘

       Table 25. Proxy options
       ┌─────────────┬────────────────────┬─────────────────────────────────────────────────────────────────────────────────────┐
       │Alias        │ Property           │ Note                                                                                │
       ├─────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │method       │ proxy.method       │                                                                                     │
       ├─────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │browser-only │ proxy.browser-only │                                                                                     │
       ├─────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │pac-url      │ proxy.pac-url      │                                                                                     │
       ├─────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
       │pac-script   │ proxy.pac-script   │ Read the JavaScript PAC (proxy auto-config) script from file or pass it directly on │
       │             │                    │ the command line. Prefix the value with "file://" or "js://" to force one or the    │
       │             │                    │ other.                                                                              │
       └─────────────┴────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘

    """





class NetWorkManagerException(Exception):
    def __init__(self, *args, data=None):
        Exception.__init__(self, *args)
        self.data = data

    def __repr__(self) -> str:
        return f"<{super().__repr__().replace('<', '').replace('>', '')} : {repr(self.data)}>"

    def __str__(self) -> str:
        return f"<{super().__str__().replace('<', '').replace('>', '')} : {str(self.data)}>"





class ROOT(object):
    __root__: str = 'nmcli'
    __base_command__: str
    _splitter = re.compile(r'(?<!\\):')
    def __init__(self, base: str ):
        self.__base_command__ = base

    @staticmethod
    def _sanitize_args(args) -> str or [str]:
        def sanitize_arg(arg):
            if isinstance(arg, bool):
                return str(arg).lower()

            if isinstance(arg, int):
                return str(arg)

            # if arg is not None:
            if isinstance(arg, str):
                return arg.lower()

            return arg

        if isinstance(args, (list, tuple)):
            new_args = []
            for arg in args:
                new_args.append(sanitize_arg(arg))
            return new_args
        else:
            return sanitize_arg(args)

    # noinspection PyMethodMayBeStatic
    def Shell(self, command: [str]) -> (int, str, str):
        """
            Execute args and returns status code, stdout and stderr

        Any exceptions in running subprocess are allowed to raise to caller
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        retcode = process.returncode

        return retcode, stdout.decode(), stderr.decode()

    def _execute_nmcli(self, obj, command=None, fields=None, multiline=False) -> Result:
        """  Wraps nmcli execution  """
        if fields is None:
            fields = NMCLI_FIELDS[obj]

        if "list" in command and "id" in command:
            multiline = True
            fields = NMCLI_FIELDS["%s list" % obj]

        if command:
            if ("%s %s" % (obj, command)) in NMCLI_FIELDS:
                fields = NMCLI_FIELDS[("%s %s" % (obj, command))]

        args = [self.__root__, '--terse', '--fields', ",".join(fields), obj]

        if command:
            args += shlex.split(command)

        retcode, stdout, stderr = self.Shell(args)
        data = []
        if error_codes.IsOk(retcode):
            if multiline:
                row = { }
                for line in stdout.split('\n'):
                    values = line.split(':', 1)
                    if len(values) == 2:
                        multikey, value = values
                        field, prop = multikey.split('.')
                        row[prop] = value
                data.append(row)
            else:
                for line in stdout.split('\n'):
                    values = self._splitter.split(line)
                    if len(values) == len(fields):
                        row = dict(zip(fields, values))
                        data.append(row)

            return Result(data, retcode, stdout, stderr)
        else:
            msg = f"nmcli return {retcode} code. STDERR='{stderr}'"
            raise NetWorkManagerException(msg, data={'stderr': stderr, 'retcode': retcode, 'stdout': stdout})

    def _run_action(self, command, *args, **kwargs) -> Result:
        cmd_args = [self._sanitize_args(arg) for arg in args]
        if kwargs:
            cmd_args.extend(kwargs.keys())

        if not cmd_args:
            cmd = command
        else:
            opts = []
            for arg in cmd_args:
                if arg not in kwargs:
                    opts.append(arg)
                else:
                    opts.append(f"{arg} {self._sanitize_args(kwargs[arg])}")
            cmd = f"{command} {' '.join(opts)}"

        return self._execute_nmcli(self.__root__, command=cmd)


    # def gen_action(self, command, possibleargs):
    #     def sanitize_args(args):
    #         def sanitize_arg(arg):
    #             if isinstance(arg, bool):
    #                 return str(arg).lower()
    #
    #             if isinstance(arg, int):
    #                 return str(arg)
    #
    #             if arg is not None:
    #                 return arg.lower()
    #
    #             return arg
    #
    #         if isinstance(args, list):
    #             newargs = []
    #             for arg in args:
    #                 newargs.append(sanitize_arg(arg))
    #             return newargs
    #         else:
    #             return sanitize_arg(args)
    #
    #     usableargs = sanitize_args(possibleargs)
    #
    #     def verify_arg(arg):
    #         arg = sanitize_args(arg)
    #         if arg not in usableargs:
    #             raise Exception(
    #                 "%s is not a valid argument for '%s'. Parameters: %s" % (
    #                     arg, command, possibleargs))
    #         return arg
    #
    #     def verify_args(args):
    #         return [verify_arg(arg) for arg in args]
    #
    #     def run_action(args=None, **kwargs):
    #         if args is None:
    #             args = []
    #
    #         if not isinstance(args, list):
    #             args = [args]
    #
    #         if kwargs:
    #             args.extend(kwargs.keys())
    #
    #         args = verify_args(args)
    #
    #         if not args:
    #             cmd = command
    #         else:
    #             opts = []
    #             for arg in args:
    #                 if arg not in kwargs:
    #                     opts.append(arg)
    #                 else:
    #                     opts.append("%s %s" % (arg, sanitize_args(kwargs[arg])))
    #             cmd = "%s %s" % (command, ' '.join(opts))
    #
    #         return self._execute_nmcli(self.cmdname, command=cmd)
    #
    #     return run_action

