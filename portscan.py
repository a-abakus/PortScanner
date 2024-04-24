import queue
import socket
import optparse
import sys
import threading
from os import system
from click import echo
from sys import platform
from colorama import Fore
from pyfiglet import figlet_format


YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
GREEN = Fore.GREEN
RED = Fore.RED
port_list = []
q = queue.Queue()


def print_bannner():
    ascii_banner = figlet_format("PortScanner")
    print(ascii_banner)


def help_page():
    print_bannner()
    print("""Usage: portscan.py -i 10.10.10.10 -p 22
       portscan.py -d scanme.com -p all

Options:
  -h, --help     show this help message and exit
  -d DOMAIN      enter a domain
                    or
  -i IP_ADDRESS  enter an ip address
  -p PORT        for all ports type > all
                 for single ports > 22""")


def args_():
    try:
        port_text = f"""for all ports type > all{(" " * 9) * 4}
        for single ports > 22"""
        parse_obj = optparse.OptionParser()
        parse_obj.add_option("-h", "--help", dest="", help="show this help message")
        parse_obj.add_option("-d", "", dest="domain", help="enter a domain")
        parse_obj.add_option("-i", "", dest="ip_address", help="enter an ip address")
        parse_obj.add_option("-p", dest="port", help=port_text)
        (user_input, arguments) = parse_obj.parse_args()

        try:
            if user_input.port == "all" or int(user_input.port):
                pass
        except ValueError:
            help_page()
            sys.exit()

        if user_input.ip_address:
            address = user_input.ip_address
        else:
            address = socket.gethostbyname(user_input.domain)

        if not address or not user_input.port:
            help_page()
            sys.exit()

        return address, user_input.port
    except Exception as e:
        help_page()
        sys.exit()


def get_banner(s, port):
    try:
        s.settimeout(1)
        banner = s.recv(100).decode().replace('\n', '')
        if banner != "":
            echo(f"{GREEN} -> {port} : open -> {banner}")
    except Exception as e:
        echo(f"{GREEN} -> {port} : open -> no banner")


def single_port():
    scanning()
    port = int(PORT_NUMBER)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((IP_ADRESS, port))
            get_banner(s, port)
        except Exception as e:
            print(f"{GREEN} -> {port} : close")


def multiple_ports():
    while not q.empty():
        port = q.get()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((IP_ADRESS, port))
                port_list.append(port)
                get_banner(s, port)
            except Exception as e:
                pass
        q.task_done()


def scanning():
    if platform == "win32":
        system("cls")
    # elif platform == "linux" or platform == "linux2":
    #     system("clear")
    else:
        system("clear")
    print_bannner()
    if PORT_NUMBER == "all":
        print(f"""{RED}[*] IP address : {WHITE}{IP_ADRESS}\n{RED}[*] Port(s) : {WHITE}Scanning all ports..\n""")
    else:
        print(f"""{RED}[*] IP address : {WHITE}{IP_ADRESS}\n{RED}[*] Port(s) : {WHITE}{PORT_NUMBER}\n""")


def hostisup():
    if not IP_ADRESS:
        return
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((IP_ADRESS, 22))
            flag1 = True
    except (socket.timeout, OSError):
        flag1 = False
    except ConnectionRefusedError:
        flag1 = True
    return flag1


def main():
    if PORT_NUMBER == "all":
        port_start = 1
        port_finish = 65536
        scanning()
        try:
            for i in range(port_start, port_finish):
                q.put(i)
            for i in range(50):
                t = threading.Thread(target=multiple_ports, daemon=True)
                t.start()
            q.join()
            print(f"\n{YELLOW}-> {len(port_list)} ports open..")
            print(f"\n{RED}Scan is done!")
        except KeyboardInterrupt:
            print(f"\n{RED}Exitting..")
            sys.exit()
    else:
        single_port()
        print(f"\n{RED}Scan is done.!")


if __name__ == "__main__":
    IP_ADRESS, PORT_NUMBER = args_()
    flag_ = hostisup()
    if flag_:
        main()
    else:
        print(f"\n{YELLOW}{IP_ADRESS} : TARGET is DOWN.!")
        sys.exit()
