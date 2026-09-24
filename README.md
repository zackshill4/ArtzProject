# ARTZ Terminal Toolkit

Local terminal toolkit for Termux, Windows Terminal, and Linux.

## Commands
- `base64` encode/decode
- `enc` SHA-256 digest
- `deobfuscated` safely unescape text; never executes input
- `string` extract quoted strings
- `check-ip` simulated IP profile
- `check-address` simulated fictional address
- `check-device` simulated device profile with a non-identifying series code

The three check commands are explicitly simulated and do not query real location, network, or device-fingerprint data.

## Usage
```bash
python artz.py --help
python artz.py base64 "ARTZ"
python artz.py base64 "QVJUWg==" --decode
python artz.py enc "ARTZ"
python artz.py deobfuscated "\\x41\\x52\\x54\\x5a"
python artz.py string 'name="ARTZ" mode="terminal"'
python artz.py check-ip
python artz.py check-address
python artz.py check-device
```

Windows: `run_artz.bat check-device`

Termux/Linux:
```sh
chmod +x run_artz.sh
./run_artz.sh check-device
```
