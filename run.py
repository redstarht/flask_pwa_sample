import socket
import os

from app import create_app

app = create_app()

cert_file = os.path.join(os.path.dirname(__file__), 'server.crt')
key_file = os.path.join(os.path.dirname(__file__), 'server.key')
print("cert exists:", os.path.exists(cert_file))
print("key exists:", os.path.exists(key_file))
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"IP:{ip_address}")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=443,ssl_context=(cert_file, key_file))