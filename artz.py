#!/usr/bin/env python3
"""ARTZ Terminal Toolkit: local utilities and explicitly simulated profiles."""

from __future__ import annotations

import argparse
import base64
import hashlib
import re
import sys
from codecs import decode as codec_decode

ART = r"""
 █████╗ ██████╗ ████████╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝╚══███╔╝
███████║██████╔╝   ██║     ███╔╝
██╔══██║██╔══██╗   ██║    ███╔╝
██║  ██║██║  ██║   ██║   ███████╗
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
"""

SERIES = "ARTZ-SIM-2026-7F3A"

def b64(value: str, decode: bool) -> str:
    if decode:
        try:
            return base64.b64decode(value, validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError("input is not valid UTF-8 Base64") from exc
    return base64.b64encode(value.encode("utf-8")).decode("ascii")

def enc(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def deobfuscated(value: str) -> str:
    try:
        return codec_decode(value, "unicode_escape")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid escaped text") from exc

def strings(value: str) -> list[str]:
    pattern = r'''(?:"([^"\\]*(?:\\.[^"\\]*)*)"|'([^'\\]*(?:\\.[^'\\]*)*)')'''
    return [a if a else b for a, b in re.findall(pattern, value)]

def fake_ip() -> None:
    print("IP PROFILE  [SIMULATED]")
    print("address : 203.0.113.42")
    print("note    : documentation-only TEST-NET address; no lookup performed")

def fake_address() -> None:
    print("ADDRESS PROFILE  [SIMULATED]")
    print("address : 42 Example Circuit, ARTZ District")
    print("note    : fictional address; no geolocation performed")

def fake_device() -> None:
    print("DEVICE PROFILE  [SIMULATED]")
    print(f"series  : {SERIES}")
    print("model   : ARTZ-Terminal Virtual Node")
    print("status  : synthetic profile; no device fingerprinting performed")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="artz", description="ARTZ local terminal toolkit")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("base64"); p.add_argument("value"); p.add_argument("--decode", action="store_true")
    p = sub.add_parser("enc"); p.add_argument("value")
    p = sub.add_parser("deobfuscated"); p.add_argument("value")
    p = sub.add_parser("string"); p.add_argument("value")
    sub.add_parser("check-ip"); sub.add_parser("check-address"); sub.add_parser("check-device")
    return parser

def main() -> int:
    print(ART)
    args = build_parser().parse_args()
    try:
        if args.command == "base64": print(b64(args.value, args.decode))
        elif args.command == "enc": print(enc(args.value))
        elif args.command == "deobfuscated": print(deobfuscated(args.value))
        elif args.command == "string":
            result = strings(args.value)
            print("\n".join(result) if result else "No quoted strings found.")
        elif args.command == "check-ip": fake_ip()
        elif args.command == "check-address": fake_address()
        elif args.command == "check-device": fake_device()
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
