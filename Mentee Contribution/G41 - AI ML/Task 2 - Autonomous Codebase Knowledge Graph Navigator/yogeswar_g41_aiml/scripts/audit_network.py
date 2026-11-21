import socket

hostname = socket.gethostname()
ips = socket.gethostbyname_ex(hostname)[2]
print(f"Hostname: {hostname}")
print(f"Host IPs: {ips}")

for ip in ips:
    for port in [80, 443]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        try:
            res = s.connect_ex((ip, port))
            status = "OPEN / REACHABLE" if res == 0 else f"CLOSED / BLOCKED (code {res})"
            print(f"Testing {ip}:{port} -> {status}")
        except Exception as e:
            print(f"Testing {ip}:{port} -> ERROR: {e}")
        finally:
            s.close()
