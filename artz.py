#!/usr/bin/env python3
"""ARTZ Terminal — cross-platform local utility console.

Real data is limited to information the operating system and public services
can safely expose: local system details, local network interfaces, and the
public IP address. Exact street address and hardware serial numbers are not
read or guessed.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import platform
import re
import socket
import ssl
import sys
import urllib.parse
import urllib.request
from codecs import decode as codec_decode
from datetime import datetime, timezone

VERSION = "2.0.0"
TIMEOUT = 6

ART = r"""
    █████╗ ██████╗ ████████╗███████╗
   ██╔══██╗██╔══██╗╚══██╔══╝╚══███╔╝
   ███████║██████╔╝   ██║     ███╔╝
   ██╔══██║██╔══██╗   ██║    ███╔╝
   ██║  ██║██║  ██║   ██║   ███████╗
   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def banner() -> None:
    print(ART)
    print(f"  ARTZ TERMINAL  v{VERSION}  |  {platform.system()} / Python {platform.python_version()}")
    print("  ─────────────────────────────────────────────────────────")

def prompt(label: str) -> str:
    return input(f"\n  {label}: ").strip()

def b64_encode(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")

def b64_decode(value: str) -> str:
    try:
        raw = base64.b64decode(value, validate=True)
        return raw.decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid UTF-8 Base64") from exc

def digest(value: str, algorithm: str = "sha256") -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as exc:
        raise ValueError(f"unsupported hash: {algorithm}") from exc
    h.update(value.encode("utf-8"))
    return h.hexdigest()

def deobfuscate(value: str) -> str:
    try:
        return codec_decode(value, "unicode_escape")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid escaped text") from exc

def extract_strings(value: str) -> list[str]:
    pattern = r'''(?:"([^"\\]*(?:\\.[^"\\]*)*)"|'([^'\\]*(?:\\.[^'\\]*)*)')'''
    return [a if a is not None else b for a, b in re.findall(pattern, value)]

def local_device() -> None:
    uname = platform.uname()
    print("\n  [DEVICE / OS]")
    rows = {
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "architecture": platform.architecture()[0],
        "processor": uname.processor or "unknown",
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
    }
    for key, value in rows.items():
        print(f"  {key:<12} {value}")

def local_network() -> None:
    print("\n  [LOCAL NETWORK]")
    host = socket.gethostname()
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, None)})
    except socket.gaierror:
        addresses = []
    print(f"  hostname     {host}")
    for address in addresses:
        print(f"  address      {address}")
    if not addresses:
        print("  address      unavailable")

def public_ip() -> str:
    request = urllib.request.Request(
        "https://api.ipify.org?format=json",
        headers={"User-Agent": "ARTZ-Terminal/2.0"},
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=TIMEOUT, context=context) as response:
        payload = json.load(response)
    ip = payload.get("ip")
    if not isinstance(ip, str) or not ip:
        raise ValueError("public IP service returned an invalid response")
    return ip

def public_ip_profile() -> None:
    ip = public_ip()
    print("\n  [PUBLIC IP]")
    print(f"  address      {ip}")
    print("  source       ipify.org")
    print("  note         public network address; not a street address")

def ip_lookup() -> None:
    ip = prompt("IP address")
    try:
        parsed = urllib.parse.urlparse(f"https://ipwho.is/{urllib.parse.quote(ip, safe=':.')}")
        request = urllib.request.Request(
            parsed.geturl(),
            headers={"User-Agent": "ARTZ-Terminal/2.0"},
        )
        context = ssl.create_default_context()
        with urllib.request.urlopen(request, timeout=TIMEOUT, context=context) as response:
            data = json.load(response)
    except Exception as exc:
        raise ValueError(f"IP lookup failed: {exc}") from exc

    if data.get("success") is False:
        raise ValueError(str(data.get("message") or "IP lookup rejected"))

    print("\n  [IP INTELLIGENCE]")
    for key in ("ip", "type", "continent", "country", "region", "city", "latitude", "longitude", "isp", "org"):
        value = data.get(key)
        if value not in (None, ""):
            print(f"  {key:<12} {value}")
    print("  note         approximate network geolocation; not an exact street address")

def timestamp() -> None:
    now = datetime.now(timezone.utc)
    print("\n  [TIME]")
    print(f"  UTC          {now.isoformat()}")
    print(f"  epoch        {int(now.timestamp())}")

def interactive() -> None:
    while True:
        clear()
        banner()
        print("""
  01  Base64 encode
  02  Base64 decode
  03  SHA-256 hash
  04  Deobfuscate escaped text
  05  Extract quoted strings
  06  Device / OS info
  07  Local network info
  08  Public IP
  09  IP geolocation
  10  UTC timestamp
  0   Exit
""")
        choice = input("  ARTZ > ").strip().lower()
        try:
            if choice == "1" or choice == "01":
                print(f"\n  result       {b64_encode(prompt('text'))}")
            elif choice == "2" or choice == "02":
                print(f"\n  result       {b64_decode(prompt('base64'))}")
            elif choice == "3" or choice == "03":
                print(f"\n  sha256       {digest(prompt('text'))}")
            elif choice == "4" or choice == "04":
                print(f"\n  result       {deobfuscate(prompt('escaped text'))}")
            elif choice == "5" or choice == "05":
                result = extract_strings(prompt('source text'))
                print("\n  strings")
                print("\n".join(f"    {item}" for item in result) if result else "    none")
            elif choice == "6" or choice == "06":
                local_device()
            elif choice == "7" or choice == "07":
                local_network()
            elif choice == "8" or choice == "08":
                public_ip_profile()
            elif choice == "9" or choice == "09":
                ip_lookup()
            elif choice == "10":
                timestamp()
            elif choice in {"0", "q", "quit", "exit"}:
                print("\n  ARTZ session closed.")
                return
            else:
                print("\n  unknown menu selection")
        except (ValueError, OSError, urllib.error.URLError) as exc:
            print(f"\n  error        {exc}")
        input("\n  Press Enter to continue...")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="artz", description="ARTZ cross-platform terminal toolkit")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("menu")
    p = sub.add_parser("base64"); p.add_argument("value"); p.add_argument("--decode", action="store_true")
    p = sub.add_parser("hash"); p.add_argument("value"); p.add_argument("--algorithm", default="sha256")
    p = sub.add_parser("deobfuscate"); p.add_argument("value")
    p = sub.add_parser("strings"); p.add_argument("value")
    sub.add_parser("device")
    sub.add_parser("network")
    sub.add_parser("public-ip")
    p = sub.add_parser("ip"); p.add_argument("address")
    sub.add_parser("time")
    return parser

def run_cli(args: argparse.Namespace) -> int:
    if args.command in (None, "menu"):
        interactive()
    elif args.command == "base64":
        print(b64_decode(args.value) if args.decode else b64_encode(args.value))
    elif args.command == "hash":
        print(digest(args.value, args.algorithm))
    elif args.command == "deobfuscate":
        print(deobfuscate(args.value))
    elif args.command == "strings":
        print("\n".join(extract_strings(args.value)))
    elif args.command == "device":
        local_device()
    elif args.command == "network":
        local_network()
    elif args.command == "public-ip":
        public_ip_profile()
    elif args.command == "ip":
        ip_lookup_value(args.address)
    elif args.command == "time":
        timestamp()
    return 0

def ip_lookup_value(address: str) -> None:
    original = input
    try:
        globals()["input"] = lambda _: address
        ip_lookup()
    finally:
        globals()["input"] = original

def main() -> int:
    clear()
    banner()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run_cli(args)
    except (ValueError, OSError, urllib.error.URLError) as exc:
        print(f"\n  error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
