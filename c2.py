import socket
import threading
import sys

clients = []
server_running = True
server = None
print_lock = threading.Lock()


def safe_print(msg):
    """Thread-safe print without adding prompt."""
    with print_lock:
        print(msg)


def handle_client(conn, addr):
    clients.append(conn)
    safe_print(f"[+] CLIENT CONNECTED FROM {addr}")
    try:
        while server_running:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                safe_print(f"[DATA FROM {addr}] {data.decode(errors='ignore')}")
            except:
                break
    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()
        safe_print(f"[-] CLIENT DISCONNECTED FROM {addr}")


def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 9999))
    server.listen()
    

    try:
        while server_running:
            try:
                server.settimeout(1.0)
                conn, addr = server.accept()
            except socket.timeout:
                continue
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    finally:
        safe_print("[*] SHUTTING DOWN SERVER...")
        for c in clients[:]:
            try:
                c.shutdown(socket.SHUT_RDWR)
                c.close()
            except:
                pass
        clients.clear()
        server.close()


def broadcast(message):
    for c in clients[:]:
        try:
            c.sendall(message.encode())
            safe_print(f"[→] SENT TO {c.getpeername()}")
        except:
            clients.remove(c)


safe_print("""
SMM COMMAND AND CONTROL SERVICE

[/s] STARTS HOSTING SERVICE
[/e] EXITS THE SERVER AND SHUTS ALL CLIENTS DOWN
[/n.o] SHOWS HOW MANY CLIENTS ARE CONNECTED TO THE SERVER
[/b] BROADCASTS A MESSAGE TO ALL CONNECTED CLIENTS
""")


while True:
    try:
        command = input("root@: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        safe_print("[*] EXITING SERVER...")
        server_running = False
        if server:
            server.close()
        break

    if command == "/s":
        if not server_running:
            server_running = True
        safe_print("STARTING C2 CLIENTS WILL CONNECT...")
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        safe_print("[*] C2 SERVER IS LIVE AND LISTENING ON PORT 9999")

    elif command == "/n.o":
        safe_print(f"[*] CONNECTED CLIENTS: {len(clients)}")

    elif command == "/e":
        safe_print("[*] EXITING SERVER AND DISCONNECTING ALL CLIENTS...")
        server_running = False
        if server:
            server.close()
        break

    elif command == "/b":
        msg = input("root@msg: ")
        broadcast(msg)
        safe_print("[*] MESSAGE SENT TO ALL CLIENTS.")

    elif command == "":
        continue

    else:
        safe_print("INCORRECT COMMAND!")
