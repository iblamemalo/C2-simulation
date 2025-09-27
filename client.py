import socket
import time
import sys

server_ip = "127.0.0.1"
server_port = 9999

def connect_to_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        print("[+] CONNECTED TO C2 SERVER")

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    print("[-] SERVER CLOSED CONNECTION.")
                    break
                print(f"[SERVER] {data.decode(errors='ignore')}")
            except ConnectionResetError:
                print("[-] CONNECTION RESET BY SERVER.")
                break
            except Exception as e:
                print(f"[!] ERROR: {e}")
                break

    except Exception as e:
        print(f"[!] CONNECTION FAILED: {e}")
        time.sleep(5)

while True:
    choice = input("DO YOU WANT TO CONNECT TO THE SERVER? (Y/N): ").strip().lower()

    if choice == 'y':
        connect_to_server()
        break
    elif choice == 'n':
        print("[-] CONNECTION CANCELLED BY USER.")
        sys.exit()
    else:
        print("[!] INVALID INPUT. PLEASE TYPE 'Y' OR 'N'.")
