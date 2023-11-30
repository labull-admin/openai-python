
import asyncio
import threading
import os
from sshtunnel import SSHTunnelForwarder
from loguru import logger

# Configuration
SSH_SERVER = 'proxy.labull.org'
SSH_PORT = 22  # Default SSH port
SSH_USERNAME = 'ubuntu'
SSH_KEY_PATH = os.getenv('PROXY_LABULL_ORG_SSH_KEY_PATH')
REMOTE_HOST = 'proxy.labull.org'
REMOTE_PORT = 2046  # Port of the remote proxy server

logger.debug(
    f"Connecting to {SSH_SERVER}:{SSH_PORT} with username {SSH_USERNAME} and key {SSH_KEY_PATH}")
# Establish an SSH tunnel
tunnel = SSHTunnelForwarder(
    (SSH_SERVER, SSH_PORT),
    ssh_username=SSH_USERNAME,
    ssh_pkey=SSH_KEY_PATH,
    remote_bind_address=(REMOTE_HOST, REMOTE_PORT),
    local_bind_address=('127.0.0.1', 0)  # Set to '0' to find an available port
)

# Function to start the tunnel


def start_tunnel():
    tunnel.start()
    logger.debug(f"Labull Proxy Tunnel is active on localhost:{tunnel.local_bind_port}, "
                 f"and it is forwarding to {REMOTE_HOST}:{REMOTE_PORT}")

# Function to stop the tunnel


def stop_tunnel():
    if tunnel.is_active:
        tunnel.stop()
        logger.warning("Labull Proxy Tunnel stopped")


# Asynchronous function to check and restart the tunnel
async def check_tunnel():
    while True:
        if not tunnel.is_active:
            logger.warning(
                "Labull Proxy Tunnel is not active, trying to start...")
            start_tunnel()
        await asyncio.sleep(10)  # Check every 30 seconds

# Function to run the asynchronous loop in a separate thread


def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_tunnel())


# start_tunnel
start_tunnel()
# Create a new event loop for the background thread
new_loop = asyncio.new_event_loop()
t = threading.Thread(target=run_async_loop, args=(new_loop,))
t.start()

# Now you can use the tunnel with a proxy-aware HTTP client or library.

proxies = {
    'http://': f'http://localhost:{tunnel.local_bind_port}',
    'https://': f'http://localhost:{tunnel.local_bind_port}'
}
