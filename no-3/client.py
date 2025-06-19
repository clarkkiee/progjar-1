import sys
import socket
import logging
import os

#set basic logging
logging.basicConfig(level=logging.INFO)

file_to_send = "example.txt"

try:

    if not os.path.exists(file_to_send):
        logging.error(f"Error file '{file_to_send}' not found")
        sys.exit(1)
        
    # read file
    with open(file_to_send, "rb") as f:
        file_content = f.read()
    logging.info(f"Read {len(file_content)} bytes from '{file_to_send}'")
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.16.16.101', 32444)
    logging.info(f"connecting to {server_address}")
    sock.connect(server_address)

    logging.info(f"sending {len(file_content)} bytes of file data")
    sock.sendall(file_content)
    
    amount_received = 0
    logging.info("waiting for server response")
    server_response = b""
    
    while True:
        data = sock.recv(1024) # Menerima balasan dari server
        if data:
            server_response += data
        else:
            break # Tidak ada data lagi dari server

    logging.info(f"Received response from server: {server_response.decode()}")
        
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
finally:
    logging.info("closing")
    sock.close()