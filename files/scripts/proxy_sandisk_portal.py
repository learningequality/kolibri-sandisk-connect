"""
Proxies GET and POST requests from port 8000 through to the protected Sandisk portal on port 83.
It puts a Basic HTTP Auth frontend in front of port 8000, with default creds: admin/pass
"""

import SocketServer
import SimpleHTTPServer
import urllib2

PORT = 8000

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        self.do_request()
        
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        self.do_request(data=data)

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Sandisk\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_request(self, data=None):
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            return
        elif self.headers.getheader('Authorization') != 'Basic YWRtaW46cGFzcw==': # admin/pass
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            return

        r = urllib2.urlopen("http://127.0.0.1:83" + self.path, data=data)
        self.send_response(r.code)
        for header_name, header_val in r.headers.items():
            self.send_header(header_name, header_val)
        self.end_headers()
        self.copyfile(r, self.wfile)

class TCPServerAllowingAddressReuse(SocketServer.TCPServer):
    allow_reuse_address = True

httpd = TCPServerAllowingAddressReuse(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()