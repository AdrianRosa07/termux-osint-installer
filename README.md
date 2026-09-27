# Termux OSINT Tools Installer

A comprehensive Python script to install **OSINT (Open Source Intelligence)** tools on **Termux** (Android/Linux ARM64).

## 📦 Tools Included

### 🔍 Identity & People Tracking
| Tool | Description | Method |
|------|-------------|--------|
| **Maigret** | Username enumeration across 2500+ sites with profile extraction | pip |
| **Sherlock** | Username search across 300+ social networks | git + pip |
| **Holehe** | Email verification on 100+ sites via password recovery | pip |
| **EspectroSint** | Brazilian OSINT framework (CPF, CNPJ, phones, etc.) | git + pip |

### 🌐 Infrastructure & Network Discovery
| Tool | Description | Method |
|------|-------------|--------|
| **Shodan CLI** | Search engine for Internet-connected devices | pip |
| **Amass** | Subdomain enumeration & attack surface mapping | Go |
| **theHarvester** | Emails, subdomains, employee names from public sources | git + pip |
| **Nmap** | Network discovery and security auditing | apt |
| **Wiz CLI** | Cloud security scanner | binary |

### 🕷️ Data Collection & Automation
| Tool | Description | Method |
|------|-------------|--------|
| **SpiderFoot** | Automated OSINT from 200+ data sources | git + pip |
| **Recon-ng** | Full-featured Web Reconnaissance framework | git + pip |
| **Photon** | Fast crawler for URLs, emails, social accounts, files | git + pip |

### 🔬 Forensics & Metadata
| Tool | Description | Method |
|------|-------------|--------|
| **ExifTool** | Read/write metadata in images, videos, documents | apt |
| **Metagoofil** | Extract metadata from public documents (PDF, Word) | git + pip |

## 🚀 Quick Start

### Option 1: Direct Download & Run (Recommended)
```bash
# In Termux
pkg update && pkg install -y python git curl

# Clone and run
git clone https://github.com/SEU_USUARIO/termux-osint-installer.git
cd termux-osint-installer
chmod +x termux_osint_installer.py
python3 termux_osint_installer.py
```

### Option 2: One-liner
```bash
curl -fsSL https://raw.githubusercontent.com/SEU_USUARIO/termux-osint-installer/main/termux_osint_installer.py -o termux_osint_installer.py && chmod +x termux_osint_installer.py && python3 termux_osint_installer.py
```

## 💻 Usage

### Interactive Menu (Default)
```bash
python3 termux_osint_installer.py
```

### Command Line Options
```bash
# Install all tools
python3 termux_osint_installer.py --all

# Install specific category
python3 termux_osint_installer.py --category identity-people-tracking
python3 termux_osint_installer.py --category infrastructure-network-discovery
python3 termux_osint_installer.py --category data-collection-automation
python3 termux_osint_installer.py --category forensics-metadata

# Force reinstall
python3 termux_osint_installer.py --all --force

# Show report
python3 termux_osint_installer.py --report

# Reset state
python3 termux_osint_installer.py --reset

# Custom directories
python3 termux_osint_installer.py --install-dir ~/my-osint --log-dir ~/my-logs
```

## 📁 Directory Structure
```
~/osint-tools/
├── bin/           # Symlinks to all installed tools (in PATH)
├── tools/         # Git-cloned tool repositories
└── ...

~/osint-installer-logs/
└── install_YYYYMMDD_HHMMSS.log
```

## ⚙️ Requirements

- **Termux** (Android 7.0+ or Linux ARM64)
- **Python 3.8+**
- **git**, **curl**, **wget**
- **~2-3 GB** free space for all tools
- Internet connection

### Root Access
Some tools work better with root (Nmap raw sockets, etc.) but **not required**. The script detects root and warns if needed.

## 🔧 Post-Installation

After installation, tools are available via `~/osint-tools/bin/` which is added to your PATH.

```bash
# Reload shell or source
source ~/.bashrc  # or ~/.zshrc

# Test tools
maigret --help
sherlock --help
holehe --help
nmap --version
shodan --help
amass -h
theharvester -h
python3 ~/osint-tools/tools/spiderfoot/sf.py --help
python3 ~/osint-tools/tools/recon-ng/recon-ng --help
python3 ~/osint-tools/tools/Photon/photon.py --help
exiftool -ver
python3 ~/osint-tools/tools/metagoofil/metagoofil.py -h
```

## 📝 Features

- ✅ **Resume capability** - Tracks installed tools, resumes interrupted installs
- ✅ **Multiple install methods** - apt, pip, pipx, Go, git, binary downloads
- ✅ **Dependency resolution** - Auto-installs required system packages
- ✅ **Detailed logging** - Full install logs with timestamps
- ✅ **Progress tracking** - Real-time status with durations
- ✅ **Summary report** - Complete installation report at the end
- ✅ **Category selection** - Install only what you need
- ✅ **Force reinstall** - Override existing installations
- ✅ **Termux optimized** - Handles Termux-specific paths and limitations
- ✅ **Root detection** - Warns when root is needed

## 🐛 Troubleshooting

### Go tools (Amass) fail
```bash
pkg install golang
export PATH=$PATH:~/go/bin
```

### Python packages fail
```bash
pkg install python-pip
pip3 install --upgrade pip setuptools wheel
```

### Git clone fails (shallow clone issues)
```bash
# Remove and re-run
rm -rf ~/osint-tools/tools/TOOL_NAME
```

### Permission denied
```bash
# Ensure script is executable
chmod +x termux_osint_installer.py
```

## 📋 Logs & State

- **Install logs**: `~/osint-installer-logs/install_YYYYMMDD_HHMMSS.log`
- **State file**: `~/.osint_installer_state.json` (tracks installed/failed tools)

## 🤝 Contributing

1. Fork the repository
2. Add new tools to the `TOOLS` list in `termux_osint_installer.py`
3. Test on Termux
4. Submit PR

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## ⚠️ Disclaimer

This tool installs third-party OSINT tools. Use responsibly and legally. 
Only target systems you own or have explicit permission to test.
The authors are not responsible for misuse.

## 🙏 Credits

All tools belong to their respective authors:
- Maigret: [@soxoj](https://github.com/soxoj/maigret)
- Sherlock: [@sherlock-project](https://github.com/sherlock-project/sherlock)
- Holehe: [@megadose](https://github.com/megadose/holehe)
- EspectroSint: [@EspectroSint](https://github.com/EspectroSint/EspectroSint)
- Amass: [@OWASP](https://github.com/OWASP/Amass)
- theHarvester: [@laramies](https://github.com/laramies/theHarvester)
- SpiderFoot: [@smicallef](https://github.com/smicallef/spiderfoot)
- Recon-ng: [@lanmaster53](https://github.com/lanmaster53/recon-ng)
- Photon: [@s0md3v](https://github.com/s0md3v/Photon)
- Metagoofil: [@laramies](https://github.com/laramies/metagoofil)
- And many more...