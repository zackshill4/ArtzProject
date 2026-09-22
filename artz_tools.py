#!/usr/bin/env python3
import base64, hashlib, json, os, platform, secrets, socket, sys
from pathlib import Path

RESET="\033[0m"; CYAN="\033[96m"; DIM="\033[2m"; BOLD="\033[1m"

def banner():
    print(CYAN + r"""
     █████╗ ██████╗ ████████╗███████╗
    ██╔══██╗██╔══██╗╚══██╔══╝╚══███╔╝
    ███████║██████╔╝   ██║     ███╔╝
    ██╔══██║██╔══██╗   ██║    ███╔╝
    ██║  ██║██║  ██║   ██║   ███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
        [ ARTZ TERMINAL // TOOLKIT ]
    """ + RESET)

def info():
    print(f"{BOLD}System Info{RESET}")
    print("OS      :", platform.system(), platform.release())
    print("Machine :", platform.machine())
    print("Python  :", platform.python_version())
    print("Host    :", socket.gethostname())

def hash_file():
    p = input("File path: ").strip()
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        print("SHA-256 :", h.hexdigest())
    except Exception as e:
        print("Error   :", e)

def b64():
    mode = input("[1] Encode  [2] Decode: ").strip()
    data = input("Text: ")
    try:
        if mode == "1":
            print(base64.b64encode(data.encode()).decode())
        elif mode == "2":
            print(base64.b64decode(data).decode())
        else:
            print("Invalid option.")
    except Exception as e:
        print("Error:", e)

def json_format():
    raw = input("JSON: ")
    try:
        print(json.dumps(json.loads(raw), indent=2, ensure_ascii=False))
    except Exception as e:
        print("Invalid JSON:", e)

def token():
    n = input("Length [32]: ").strip()
    try: n = max(8, min(int(n or 32), 128))
    except ValueError: n = 32
    print(secrets.token_urlsafe(n)[:n])

def local_net():
    try:
        host = socket.gethostname()
        print("Hostname :", host)
        print("Local IP :", socket.gethostbyname(host))
    except Exception as e:
        print("Error:", e)

def main():
    while True:
        banner()
        print(DIM + "Safe utilities • local-only • no exploit functions" + RESET)
        print("""
 [1] System info
 [2] SHA-256 file hash
 [3] Base64 encoder/decoder
 [4] JSON formatter
 [5] Secure random token
 [6] Local network info
 [0] Exit
""")
        c = input("ARTZ@terminal > ").strip()
        if c == "1": info()
        elif c == "2": hash_file()
        elif c == "3": b64()
        elif c == "4": json_format()
        elif c == "5": token()
        elif c == "6": local_net()
        elif c == "0":
            print("ARTZ offline. Bye.")
            break
        else:
            print("Unknown command.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
