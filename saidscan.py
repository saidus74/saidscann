import socket
import ipaddress
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

CHECK_PORTS = [22, 80, 443, 8080]
TIMEOUT = 0.4
scan_results = []
mutex = Lock()


def show_title():
    print("\n--- Network Host & Port Kontrol Aracı ---\n")


def host_alive(ip):
    system = platform.system()

    if system == "Windows":
        cmd = ["ping", "-n", "1", "-w", "800", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    return subprocess.call(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0


def check_ports(ip):
    found = []

    for p in CHECK_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIMEOUT)
                if sock.connect_ex((ip, p)) == 0:
                    found.append(p)
        except:
            continue

    return found


def analyze_ip(ip):
    ip = str(ip)

    if host_alive(ip):
        ports = check_ports(ip)
        ports_str = " ".join(map(str, ports)) if ports else "YOK"
        with mutex:
            scan_results.append([ip, "AKTİF", ports_str])
    else:
        with mutex:
            scan_results.append([ip, "ERİŞİLEMEDİ", "-"])


def scan_subnet(subnet):
    net = ipaddress.ip_network(subnet, strict=False)

    with ThreadPoolExecutor(max_workers=40) as pool:
        for host in net.hosts():
            pool.submit(analyze_ip, host)


def show_results():
    print("{:<16} {:<12} {:<20}".format("IP", "DURUM", "PORTLAR"))
    print("-" * 48)

    for row in sorted(scan_results):
        print("{:<16} {:<12} {:<20}".format(row[0], row[1], row[2]))


if __name__ == "__main__":
    show_title()
    target_net = input("Taranacak ağ (örn: 10.10.10.0/24): ")
    scan_subnet(target_net)
    show_results()
