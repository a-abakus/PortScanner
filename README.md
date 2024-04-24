# Port Scanner
Port Scanner is a tool used to test TCP connections on a specified IP address or domain name. This tool can check a specific port or be used to scan all ports on the specified IP address or domain.

## Usage
```
pip3 install -r requirements.txt

python3 portscan.py -i <192.168.1.10> -p <22>
```

### Options
- `-h, --help`: Show help message and exit.
- `-i ip address`: Enter the IP address.
- `-d domain`: Enter the domain.
- `-p port`: Type `all` for all ports or enter a single port number.

## Example
```
python3 portscan.py -i 192.168.1.10 -p all

 ____            _   ____                                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
|  __/ (_) | |  | |_ ___) | (_| (_| | | | | | | |  __/ |   
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|_| |_|\___|_|       

[*] IP address : 192.168.1.10
[*] Port(s) : Scanning all ports..

 -> 22 : open -> SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
 -> 80 : open -> no banner

^C
Exitting..
```
