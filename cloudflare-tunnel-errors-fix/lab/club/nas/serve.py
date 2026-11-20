# The club's photo NAS: a small HTTPS server with a self-signed certificate, like a NAS's own web page.
import http.server, ssl
srv = http.server.ThreadingHTTPServer(("", 443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("/nas/cert.pem", "/nas/key.pem")
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
srv.serve_forever()
