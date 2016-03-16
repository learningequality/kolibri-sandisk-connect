"""
Redirects all requests coming into port 80 to http://192.168.11.1:8008/
First verifies that the KA Lite server is running, and displays loading screen if needed.
"""

import BaseHTTPServer, urllib2

loading_page = """
<html>
<head>
<meta http-equiv="refresh" content="5">
</head>
<body>
<h2>KA Lite has not yet loaded. Please wait...</h2>
</body>
</html>
"""

class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(302)
        self.send_header("Location", "http://192.168.11.1:8008/")
        self.end_headers()

    def do_GET(self):
        try:
            urllib2.urlopen("http://127.0.0.1:8008/").read()
        except:
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(loading_page)
            return
        self.do_HEAD()

if __name__ == '__main__':
    try:
        httpd = BaseHTTPServer.HTTPServer(("", 80), RedirectHandler)
    except:
        # print "Port 80 is in use or could not be acquired; exiting redirect script."
        exit(1)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()