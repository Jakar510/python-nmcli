
NMCLI_FIELDS = {
         'nm': [
                'RUNNING',
                'STATE',
                'WIFI-HARDWARE',
                'WIFI',
                'WWAN-HARDWARE',
                'WWAN'
                 ],
         'con': [
                'NAME',
                'UUID',
                'TYPE',
                'TIMESTAMP-REAL'
                 ],
         'dev': [
                 'DEVICE',
                 'TYPE',
                 'STATE'
                 ],
         'con list': [
                'connection',
                '802-3-ethernet',
                '802-1x',
                '802-11-wireless',
                '802-11-wireless-security',
                'ipv4',
                'ipv6',
                'serial',
                'ppp',
                'pppoe',
                'gsm',
                'cdma',
                'bluetooth',
                '802-11-olpc-mesh',
                'vpn',
                'infiniband',
                'bond',
                'vlan'],
         'dev wifi': [
                'SSID',
                'BSSID',
                'MODE',
                'FREQ',
                'RATE',
                'SIGNAL',
                'SECURITY',
                'WPA-FLAGS',
                'RSN-FLAGS',
                'DEVICE',
                'ACTIVE',
                'DBUS-PATH'],
         'dev list': [
                'GENERAL',
                'CAPABILITIES',
                'BOND',
                'VLAN',
                'CONNECTIONS',
                'WIFI-PROPERTIES',
                'AP',
                'WIRED-PROPERTIES',
                'IP4',
                'DHCP4',
                'IP6',
                'DHCP6'
                 ],
         'nm permissions': [
                 'PERMISSION',
                 'VALUE'
                 ]
        }