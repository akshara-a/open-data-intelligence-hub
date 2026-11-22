import subprocess
import json

output = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"]).decode().strip().splitlines()

print(f"{'Container Name':<55} | {'Port Bindings'}")
print("-" * 85)

for c_name in output:
    c_name = c_name.strip()
    if not c_name:
        continue
    raw_ports = subprocess.check_output(["docker", "inspect", c_name, "--format", "{{json .NetworkSettings.Ports}}"]).decode().strip()
    try:
        ports = json.loads(raw_ports)
        published = []
        for container_port, host_bindings in (ports or {}).items():
            if host_bindings:
                for b in host_bindings:
                    published.append(f"{container_port} -> {b.get('HostIp')}:{b.get('HostPort')}")
            else:
                published.append(f"{container_port} (internal only)")
        pub_str = ", ".join(published) if published else "None (internal only)"
    except Exception as e:
        pub_str = f"Error parsing ports: {e}"
    print(f"{c_name:<55} | {pub_str}")
