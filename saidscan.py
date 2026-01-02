import socket

def host_kontrol(ip, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False


def main():
    print("=== Network Host Tespit Aracı (Socket) ===\n")

    ip_base = input("IP bloğunu gir (örn: 192.168.1): ")
    baslangic = int(input("Başlangıç host numarası: "))
    bitis = int(input("Bitiş host numarası: "))
    port = int(input("Kontrol edilecek port (örn: 80): "))

    print("\nTarama başlıyor...\n")

    aktif_hostlar = []

    for i in range(baslangic, bitis + 1):
        ip = f"{ip_base}.{i}"
        if host_kontrol(ip, port):
            print(f"[+] {ip} erişilebilir")
            aktif_hostlar.append(ip)
        else:
            print(f"[-] {ip} erişilemiyor")

    print("\n=== Tarama Sonucu ===")
    if aktif_hostlar:
        for host in aktif_hostlar:
            print(f"✔ {host}")
    else:
        print("Aktif host bulunamadı")


if __name__ == "__main__":
    main()
