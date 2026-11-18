# A waiter's tablet: connects to the kitchen screen and sends each order given on the command line.
import socket
import sys

tab = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tab.connect(("kitchen", 9000))
me, kitchen = tab.getsockname(), tab.getpeername()
print(f"connected: {me[0]}:{me[1]} -> {kitchen[0]}:{kitchen[1]}")
for order in sys.argv[1:]:
    tab.sendall((order + "\n").encode())
    print("sent:", order)
try:
    while tab.recv(1024):                        # stay connected until the kitchen hangs up
        pass
    print("the kitchen closed the connection")
except KeyboardInterrupt:
    print("\ntablet closing")
tab.close()
