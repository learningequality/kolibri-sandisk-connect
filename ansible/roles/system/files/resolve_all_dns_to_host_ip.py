"""
Simple DNS server, which resolves all DNS requests to our access point's IP.
"""

import socket

HOST_IP = '192.168.11.1'    # This is the IP to which all DNS queries will be resolved
LISTEN_IP = '127.0.0.1'     # This is the local IP where our DNS server will listen

udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udps.bind((LISTEN_IP, 53))

class DNSQuery:

    def __init__(self, data):
        self.data = data
        self.domain = ''

        query_type = (ord(data[2]) >> 3) & 15                               # Opcode bits
        if query_type == 0:                                                 # Standard query
            ini = 12
            lon = ord(data[ini])
            while lon != 0:
                self.domain += data[ini+1:ini+lon+1] + '.'
                ini += lon+1
                lon = ord(data[ini])

    def request(self, ip):
        packet = ''
        if self.domain:
            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]                                        # Original Domain Name Question
            packet += '\xc0\x0c'                                            # Pointer to domain name
            packet += '\x00\x01'                                            # Response type
            packet += '\x00\x01'                                            # Response class
            packet += '\x00\x00\x00\x00'                                    # TTL
            packet += '\x00\x04'                                            # resource data length -> 4 bytes
            packet += "".join([chr(int(x)) for x in ip.split('.')])         # 4bytes of IP
        return packet

try:
    while True:
        data, addr = udps.recvfrom(1024)
        p = DNSQuery(data)
        udps.sendto(p.request(HOST_IP), addr)
        print 'Returning DNS record: %s -> %s' % (p.domain, HOST_IP)
except KeyboardInterrupt:
    udps.close()
