

from typing import Union, Dict
import httpx
import os
from sshtunnel import SSHTunnelForwarder


# Configuration
SSH_SERVER = 'proxy.labull.org'
SSH_PORT = 22  # Default SSH port
SSH_USERNAME = 'ubuntu'
SSH_KEY_PATH = os.getenv('PROXY_LABULL_ORG_SSH_KEY_PATH')
REMOTE_HOST = 'proxy.labull.org'
REMOTE_PORT = 2046  # Port of the remote proxy server

# Establish an SSH tunnel
tunnel = SSHTunnelForwarder(
    (SSH_SERVER, SSH_PORT),
    ssh_username=SSH_USERNAME,
    ssh_pkey=SSH_KEY_PATH,
    remote_bind_address=(REMOTE_HOST, REMOTE_PORT),
    local_bind_address=('127.0.0.1', 0)  # Set to '0' to find an available port
)

# Start the tunnel
tunnel.start()

print(f"Tunnel is active on localhost:{tunnel.local_bind_port}, "
      f"and it is forwarding to {REMOTE_HOST}:{REMOTE_PORT}")

# Now you can use the tunnel with a proxy-aware HTTP client or library.

proxies= {
    'http://': f'http://localhost:{tunnel.local_bind_port}',
    'https://': f'http://localhost:{tunnel.local_bind_port}'
}


