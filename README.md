# OS#NT$

Public-data OSINT CLI for Termux, Windows, and Linux. The OSINT module is encrypted in `OSNT.py.enc`.

## What it does

`OS#NT$` collects publicly available technical metadata for a domain or URL:
- DNS/IP resolution
- HTTP response metadata and headers
- TLS certificate metadata
- RDAP domain data
- Certificate-Transparency names from crt.sh

Use it only on domains/systems you are authorized to inspect and respect applicable laws and service terms.

## Termux

Install Python, OpenSSL, and the Python HTTP dependency:

```sh
pkg update
pkg install python openssl
python -m pip install requests
```

Decrypt the source using the password supplied separately:

```sh
export OSNT_PASSWORD='YOUR_PASSWORD'
base64 -d OSNT.py.enc | openssl enc -d -aes-256-cbc -pbkdf2 -pass env:OSNT_PASSWORD > osnt.py
python osnt.py --help
python osnt.py example.com
python osnt.py example.com --json
```

## Windows

Install Python and OpenSSL, then install the dependency:

```powershell
py -m pip install requests
$env:OSNT_PASSWORD='YOUR_PASSWORD'
```

Decrypt:

```powershell
[IO.File]::WriteAllBytes('OSNT.bin',[Convert]::FromBase64String((Get-Content -Raw .\OSNT.py.enc)))
openssl enc -d -aes-256-cbc -pbkdf2 -in OSNT.bin -out osnt.py -pass env:OSNT_PASSWORD
py osnt.py --help
py osnt.py example.com
py osnt.py example.com --json
```

Delete `OSNT.bin` after decryption if you do not need it.

## Existing ARTZ toolkit

The original `artz.py`, `run_artz.bat`, and `run_artz.sh` remain available for the existing terminal utilities.

## Encryption

`OSNT.py.enc` uses OpenSSL AES-256-CBC with PBKDF2 and a random salt. The password is not stored in the repository.
