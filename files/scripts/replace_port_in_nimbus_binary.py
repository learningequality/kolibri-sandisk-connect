"""
One-time script that replaces the listening port in the nimbus (Sandisk portal page) binary.
Default is 80; we replace it here with port 83 (which we then protect using iptables rules at startup).
"""

NEW_PORT = 83

with open("/nimbus/nimbus") as f:
    data = f.read()

data_copy = [ch for ch in data]
data_copy[11116] = chr(NEW_PORT)
data_mod = "".join(data_copy)
with open("/nimbus/nimbus", "w") as f:
    f.write(data_mod)

