#!/usr/bin/env python3
"""
Termux OSINT Tools Verification Script
======================================
Run this AFTER the installer to verify all tools work correctly.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Tuple

# Tool verification commands
TOOLS_TO_VERIFY = [
    # Identity & People Tracking
    ("maigret", "maigret --version", "Maigret (username enumeration)"),
    ("sherlock", "python3 -m sherlock --version", "Sherlock (username search)"),
    ("holehe", "holehe --version", "Holehe (email verification)"),
    ("espectrosint", "python3 espectrosint.py --help", "EspectroSint (Brazilian OSINT)"),
    
    # Infrastructure & Network Discovery
    ("shodan", "shodan --version", "Shodan CLI"),
    ("amass", "amass version", "Amass (subdomain enum)"),
    ("theharvester", "python3 theharvester.py --version", "theHarvester"),
    ("nmap", "nmap --version", "Nmap (network scanner)"),
    ("wiz", "wiz version", "Wiz CLI"),
    
    # Data Collection & Automation
    ("spiderfoot", "python3 sf.py --version", "SpiderFoot"),
    ("recon-ng", "python3 recon-ng --version", "Recon-ng"),
    ("photon", "python3 photon.py --version", "Photon"),
    
    # Forensics & Metadata
    ("exiftool", "exiftool -ver", "ExifTool"),
    ("metagoofil", "python3 metagoofil.py --version", "Metagoofil"),
]

def run_cmd(cmd: str) -> Tuple[int, str, str]:
    """Run command and return (exit_code, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)

def check_tool(name: str, cmd: str, description: str) -> bool:
    """Check if a tool is installed and working."""
    print(f"\n🔍 Checking {description}...")
    print(f"   Command: {cmd}")
    
    # First check if binary exists in PATH
    bin_name = cmd.split()[0]
    if shutil.which(bin_name) is None:
        print(f"   ❌ NOT FOUND in PATH: {bin_name}")
        return False
    
    code, out, err = run_cmd(cmd)
    if code == 0 and out:
        version = out.split('\n')[0]
        print(f"   ✅ WORKING: {version}")
        return True
    elif code == 0 and not out:
        print(f"   ✅ RUNNING (no version output)")
        return True
    else:
        print(f"   ❌ FAILED (exit {code}): {err[:200]}")
        return False

def check_path() -> bool:
    """Check if ~/osint-tools/bin is in PATH."""
    bin_path = str(Path.home() / "osint-tools" / "bin")
    path = os.environ.get("PATH", "")
    if bin_path in path:
        print(f"✅ ~/osint-tools/bin is in PATH")
        return True
    else:
        print(f"⚠️  ~/osint-tools/bin NOT in PATH")
        print(f"   Add to ~/.bashrc: export PATH=\"{bin_path}:$PATH\"")
        return False

def main():
    import os
    
    print("=" * 60)
    print("TERMUX OSINT TOOLS VERIFICATION")
    print("=" * 60)
    print(f"User: {os.environ.get('USER', 'unknown')}")
    print(f"Home: {Path.home()}")
    print(f"Termux: {'TERMUX_VERSION' in os.environ or Path('/data/data/com.termux').exists()}")
    
    # Check PATH
    check_path()
    
    # Verify each tool
    results = []
    for name, cmd, desc in TOOLS_TO_VERIFY:
        success = check_tool(name, cmd, desc)
        results.append((name, desc, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, _, s in results if s)
    total = len(results)
    
    for name, desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {desc}")
    
    print(f"\nTotal: {passed}/{total} tools working")
    
    if passed == total:
        print("\n🎉 All tools verified successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tools need attention")
        print("\nTroubleshooting tips:")
        print("  - Run: source ~/.bashrc")
        print("  - Check logs: ~/osint-installer-logs/")
        print("  - Re-run installer with --force for failed tools")
        return 1

if __name__ == "__main__":
    sys.exit(main())