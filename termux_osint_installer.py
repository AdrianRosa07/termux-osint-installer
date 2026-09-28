#!/usr/bin/env python3
"""
Termux OSINT Tools Installer
============================
A comprehensive Python script to install OSINT (Open Source Intelligence) tools
on Termux (Android/Linux ARM64).

Tools included:
- Identity/People Tracking: Maigret, Sherlock, Holehe, EspectroSint
- Infrastructure/Network Discovery: Shodan CLI, Amass, theHarvester, Nmap, Wiz CLI
- Data Collection/Automation: SpiderFoot, Recon-ng, Photon
- Forensics/Metadata: ExifTool, Metagoofil

Author: OSINT Toolkit
License: MIT
"""

import os
import sys
import json
import time
import subprocess
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ─── Constants ──────────────────────────────────────────────────────────────
SCRIPT_VERSION = "1.1.0"
DEFAULT_INSTALL_DIR = Path.home() / "osint-tools"
DEFAULT_LOG_DIR = Path.home() / "osint-installer-logs"
STATE_FILE = Path.home() / ".osint_installer_state.json"

# ─── Data Classes ───────────────────────────────────────────────────────────
class InstallMethod(Enum):
    APT = "apt"
    PIP = "pip"
    PIPX = "pipx"
    GO = "go"
    GIT = "git"
    BINARY = "binary"
    COMPOSE = "compose"

class ToolCategory(Enum):
    IDENTITY = "Identity & People Tracking"
    INFRASTRUCTURE = "Infrastructure & Network Discovery"
    COLLECTION = "Data Collection & Automation"
    FORENSICS = "Forensics & Metadata"

@dataclass
class Tool:
    name: str
    description: str
    category: ToolCategory
    install_method: InstallMethod
    package_name: str = ""
    repo_url: str = ""
    binary_url: str = ""
    binary_name: str = ""
    go_package: str = ""
    pip_package: str = ""
    apt_package: str = ""
    post_install: List[str] = field(default_factory=list)
    check_cmd: str = ""
    version_cmd: str = ""
    dependencies: List[str] = field(default_factory=list)
    requires_root: bool = False
    size_mb: int = 0

@dataclass
class InstallState:
    installed: Dict[str, bool] = field(default_factory=dict)
    failed: Dict[str, str] = field(default_factory=dict)
    skipped: List[str] = field(default_factory=list)
    last_update: str = ""

@dataclass
class InstallResult:
    tool: str
    success: bool
    message: str
    duration: float
    version: str = ""

# ─── Tool Definitions ───────────────────────────────────────────────────────
TOOLS: List[Tool] = [
    # ─── Identity & People Tracking ────────────────────────────────────────
    Tool(
        name="maigret",
        description="Username enumeration across 2500+ sites with profile extraction",
        category=ToolCategory.IDENTITY,
        install_method=InstallMethod.PIP,
        pip_package="maigret",
        check_cmd="maigret --version",
        version_cmd="maigret --version",
        dependencies=["python3", "pip"],
    ),
    Tool(
        name="sherlock",
        description="Username search across 300+ social networks",
        category=ToolCategory.IDENTITY,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/sherlock-project/sherlock.git",
        post_install=["pip3 install -r requirements.txt"],
        check_cmd="python3 sherlock.py --version",
        version_cmd="python3 sherlock.py --version",
        dependencies=["python3", "pip", "git"],
    ),
    Tool(
        name="holehe",
        description="Email verification on 100+ sites via password recovery flows",
        category=ToolCategory.IDENTITY,
        install_method=InstallMethod.PIP,
        pip_package="holehe",
        check_cmd="holehe --version",
        version_cmd="holehe --version",
        dependencies=["python3", "pip"],
    ),
    Tool(
        name="espectrosint",
        description="OSINT framework for Brazilian context (CPF, CNPJ, phones, etc.)",
        category=ToolCategory.IDENTITY,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/EspectroSint/EspectroSint.git",
        post_install=["pip3 install -r requirements.txt"],
        check_cmd="python3 espectrosint.py --help",
        version_cmd="python3 espectrosint.py --version",
        dependencies=["python3", "pip", "git"],
    ),

    # ─── Infrastructure & Network Discovery ────────────────────────────────
    Tool(
        name="shodan",
        description="Search engine for Internet-connected devices",
        category=ToolCategory.INFRASTRUCTURE,
        install_method=InstallMethod.PIP,
        pip_package="shodan",
        check_cmd="shodan --version",
        version_cmd="shodan --version",
        dependencies=["python3", "pip"],
    ),
    Tool(
        name="amass",
        description="Subdomain enumeration and attack surface mapping",
        category=ToolCategory.INFRASTRUCTURE,
        install_method=InstallMethod.GO,
        go_package="github.com/owasp-amass/amass/v4/...@master",
        check_cmd="amass version",
        version_cmd="amass version",
        dependencies=["golang"],
        size_mb=50,
    ),
    Tool(
        name="theharvester",
        description="Emails, subdomains, and employee names from public sources",
        category=ToolCategory.INFRASTRUCTURE,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/laramies/theHarvester.git",
        post_install=["pip3 install -r requirements/base.txt"],
        check_cmd="python3 theharvester.py --version",
        version_cmd="python3 theharvester.py --version",
        dependencies=["python3", "pip", "git"],
    ),
    Tool(
        name="nmap",
        description="Network discovery and security auditing",
        category=ToolCategory.INFRASTRUCTURE,
        install_method=InstallMethod.APT,
        apt_package="nmap",
        check_cmd="nmap --version",
        version_cmd="nmap --version",
        dependencies=[],
    ),
    Tool(
        name="wiz",
        description="Wiz CLI for cloud security",
        category=ToolCategory.INFRASTRUCTURE,
        install_method=InstallMethod.BINARY,
        binary_url="https://github.com/wiz-sec/wiz-cli/releases/latest/download/wiz-cli-linux-arm64",
        binary_name="wiz",
        check_cmd="wiz version",
        version_cmd="wiz version",
        dependencies=["curl"],
        size_mb=30,
    ),

    # ─── Data Collection & Automation ──────────────────────────────────────
    Tool(
        name="spiderfoot",
        description="Automated OSINT collection from 200+ data sources",
        category=ToolCategory.COLLECTION,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/smicallef/spiderfoot.git",
        post_install=["pip3 install -r requirements.txt"],
        check_cmd="python3 sf.py --version",
        version_cmd="python3 sf.py --version",
        dependencies=["python3", "pip", "git", "sqlite3"],
        size_mb=100,
    ),
    Tool(
        name="recon-ng",
        description="Full-featured Web Reconnaissance framework",
        category=ToolCategory.COLLECTION,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/lanmaster53/recon-ng.git",
        post_install=["pip3 install -r REQUIREMENTS"],
        check_cmd="python3 recon-ng --version",
        version_cmd="python3 recon-ng --version",
        dependencies=["python3", "pip", "git"],
    ),
    Tool(
        name="photon",
        description="Fast crawler for URLs, emails, social accounts, files",
        category=ToolCategory.COLLECTION,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/s0md3v/Photon.git",
        post_install=["pip3 install -r requirements.txt"],
        check_cmd="python3 photon.py --version",
        version_cmd="python3 photon.py --version",
        dependencies=["python3", "pip", "git"],
    ),

    # ─── Forensics & Metadata ──────────────────────────────────────────────
    Tool(
        name="exiftool",
        description="Read/write metadata in images, videos, documents",
        category=ToolCategory.FORENSICS,
        install_method=InstallMethod.APT,
        apt_package="libimage-exiftool-perl",
        check_cmd="exiftool -ver",
        version_cmd="exiftool -ver",
        dependencies=[],
    ),
    Tool(
        name="metagoofil",
        description="Extract metadata from public documents (PDF, Word, etc.)",
        category=ToolCategory.FORENSICS,
        install_method=InstallMethod.GIT,
        repo_url="https://github.com/laramies/metagoofil.git",
        post_install=["pip3 install -r requirements.txt"],
        check_cmd="python3 metagoofil.py -h",
        version_cmd="python3 metagoofil.py --version",
        dependencies=["python3", "pip", "git", "exiftool"],
    ),
]

# ─── Core Installer Class ───────────────────────────────────────────────────
class TermuxOSINTInstaller:
    def __init__(self, install_dir: Path = DEFAULT_INSTALL_DIR, log_dir: Path = DEFAULT_LOG_DIR):
        self.install_dir = install_dir
        self.log_dir = log_dir
        self.tools_dir = install_dir / "tools"
        self.bin_dir = install_dir / "bin"
        self.state_file = STATE_FILE
        self.is_root = os.geteuid() == 0
        self.is_termux = self._check_termux()
        self.state = self._load_state()
        self.results: List[InstallResult] = []
        
        # Setup directories
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Add bin to PATH
        self._ensure_path()

    def _check_termux(self) -> bool:
        """Check if running in Termux environment."""
        return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ

    def _setup_logging(self):
        """Configure logging to file and console."""
        log_file = self.log_dir / f"install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        self.logger = logging.getLogger("OSINTInstaller")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        self.log_file = log_file
        self.logger.info(f"OSINT Installer v{SCRIPT_VERSION} started")
        self.logger.info(f"Install directory: {self.install_dir}")
        self.logger.info(f"Termux detected: {self.is_termux}")
        self.logger.info(f"Running as root: {self.is_root}")

    def _ensure_path(self):
        """Ensure bin directory is in PATH."""
        bin_path = str(self.bin_dir)
        if bin_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{bin_path}:{os.environ.get('PATH', '')}"

    def _load_state(self) -> InstallState:
        """Load installation state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                return InstallState(**data)
            except Exception as e:
                self.logger.warning(f"Failed to load state: {e}")
        return InstallState()

    def _save_state(self):
        """Save installation state to file."""
        self.state.last_update = datetime.now().isoformat()
        try:
            with open(self.state_file, 'w') as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")

    def _run_cmd(self, cmd: List[str], cwd: Optional[Path] = None, 
                 timeout: int = 300, check: bool = True) -> Tuple[int, str, str]:
        """Run a command and return (exit_code, stdout, stderr)."""
        self.logger.debug(f"Running: {' '.join(cmd)} (cwd: {cwd})")
        try:
            result = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
            )
            if result.stdout:
                self.logger.debug(f"STDOUT: {result.stdout[:500]}")
            if result.stderr:
                self.logger.debug(f"STDERR: {result.stderr[:500]}")
            if check and result.returncode != 0:
                self.logger.error(f"Command failed: {' '.join(cmd)}")
                self.logger.error(f"Exit code: {result.returncode}")
                self.logger.error(f"Stderr: {result.stderr}")
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {' '.join(cmd)}")
            return -1, "", "Timeout"
        except Exception as e:
            self.logger.error(f"Command error: {e}")
            return -1, "", str(e)

    def _check_tool_installed(self, tool: Tool) -> Tuple[bool, str]:
        """Check if a tool is already installed and get version."""
        if not tool.check_cmd:
            return False, ""
        
        code, out, err = self._run_cmd(tool.check_cmd.split(), check=False)
        if code == 0:
            version = out.strip().split('\n')[0] if out else "unknown"
            return True, version
        return False, ""

    def _install_apt(self, tool: Tool) -> Tuple[bool, str]:
        """Install via apt package manager."""
        self.logger.info(f"Installing {tool.name} via apt...")
        
        # Update package list
        code, _, _ = self._run_cmd(["apt", "update"], timeout=120)
        if code != 0:
            return False, "Failed to update apt package list"
        
        # Install package
        pkg = tool.apt_package or tool.name
        code, out, err = self._run_cmd(["apt", "install", "-y", pkg], timeout=300)
        if code == 0:
            return True, f"Installed {pkg} via apt"
        return False, f"Apt install failed: {err}"

    def _install_pip(self, tool: Tool) -> Tuple[bool, str]:
        """Install via pip."""
        self.logger.info(f"Installing {tool.name} via pip...")
        
        pkg = tool.pip_package or tool.name
        code, out, err = self._run_cmd(["pip3", "install", "--upgrade", pkg], timeout=300)
        if code == 0:
            return True, f"Installed {pkg} via pip"
        return False, f"Pip install failed: {err}"

    def _install_pipx(self, tool: Tool) -> Tuple[bool, str]:
        """Install via pipx (isolated environments)."""
        self.logger.info(f"Installing {tool.name} via pipx...")
        
        # Ensure pipx is installed
        code, _, _ = self._run_cmd(["pipx", "--version"], check=False)
        if code != 0:
            code, _, _ = self._run_cmd(["pip3", "install", "pipx"], timeout=120)
            if code != 0:
                return False, "Failed to install pipx"
            self._run_cmd(["pipx", "ensurepath"], check=False)
        
        pkg = tool.pip_package or tool.name
        code, out, err = self._run_cmd(["pipx", "install", pkg], timeout=300)
        if code == 0:
            return True, f"Installed {pkg} via pipx"
        return False, f"Pipx install failed: {err}"

    def _install_go(self, tool: Tool) -> Tuple[bool, str]:
        """Install via Go."""
        self.logger.info(f"Installing {tool.name} via Go...")
        
        # Check Go installation
        code, _, _ = self._run_cmd(["go", "version"], check=False)
        if code != 0:
            # Try to install Go via apt
            code, _, _ = self._run_cmd(["apt", "update"], timeout=120)
            code, _, _ = self._run_cmd(["apt", "install", "-y", "golang"], timeout=300)
            if code != 0:
                return False, "Failed to install Go"
        
        # Install Go package
        pkg = tool.go_package
        code, out, err = self._run_cmd(["go", "install", pkg], timeout=600)
        if code == 0:
            # Link binary to our bin directory
            go_bin = Path.home() / "go" / "bin" / tool.name
            if go_bin.exists():
                target = self.bin_dir / tool.name
                if target.exists():
                    target.unlink()
                target.symlink_to(go_bin)
            return True, f"Installed {pkg} via Go"
        return False, f"Go install failed: {err}"

    def _install_git(self, tool: Tool) -> Tuple[bool, str]:
        """Install via git clone."""
        self.logger.info(f"Installing {tool.name} via git...")
        
        tool_path = self.tools_dir / tool.name
        
        # Clone or update
        if tool_path.exists():
            self.logger.info(f"Updating existing {tool.name} repository...")
            code, _, _ = self._run_cmd(["git", "pull"], cwd=tool_path, timeout=120)
        else:
            code, _, err = self._run_cmd(
                ["git", "clone", "--depth", "1", tool.repo_url, str(tool_path)], 
                timeout=300
            )
        
        if code != 0:
            return False, f"Git clone/pull failed: {err}"
        
        # Run post-install commands
        for post_cmd in tool.post_install:
            self.logger.info(f"Running post-install: {post_cmd}")
            code, _, err = self._run_cmd(post_cmd.split(), cwd=tool_path, timeout=300)
            if code != 0:
                return False, f"Post-install failed: {err}"
        
        # Create symlink for main script if needed
        self._create_tool_symlink(tool, tool_path)
        
        return True, f"Installed {tool.name} from git"

    def _install_binary(self, tool: Tool) -> Tuple[bool, str]:
        """Install via direct binary download."""
        self.logger.info(f"Installing {tool.name} via binary download...")
        
        binary_name = tool.binary_name or tool.name
        target_path = self.bin_dir / binary_name
        
        # Download binary
        code, _, err = self._run_cmd(
            ["curl", "-L", "-o", str(target_path), tool.binary_url], 
            timeout=120
        )
        if code != 0:
            return False, f"Binary download failed: {err}"
        
        # Make executable
        target_path.chmod(0o755)
        
        return True, f"Downloaded and installed {binary_name}"

    def _create_tool_symlink(self, tool: Tool, tool_path: Path):
        """Create symlink for tool's main executable."""
        # Common entry points to check
        entry_points = [
            f"{tool.name}.py",
            f"{tool.name}",
            "main.py",
            "run.py",
            f"sf.py",  # SpiderFoot
            "recon-ng",  # Recon-ng
            "photon.py",  # Photon
            "metagoofil.py",  # Metagoofil
            "theharvester.py",  # theHarvester
            "sherlock.py",  # Sherlock
            "espectrosint.py",  # EspectroSint
        ]
        
        for entry in entry_points:
            entry_path = tool_path / entry
            if entry_path.exists():
                target = self.bin_dir / tool.name
                if target.exists():
                    target.unlink()
                target.symlink_to(entry_path)
                target.chmod(0o755)
                self.logger.info(f"Created symlink: {target} -> {entry_path}")
                break

    def install_tool(self, tool: Tool, force: bool = False) -> InstallResult:
        """Install a single tool."""
        start_time = time.time()
        
        # Check if already installed
        if not force:
            installed, version = self._check_tool_installed(tool)
            if installed:
                self.logger.info(f"{tool.name} already installed (v{version})")
                self.state.installed[tool.name] = True
                return InstallResult(
                    tool=tool.name,
                    success=True,
                    message=f"Already installed (v{version})",
                    duration=time.time() - start_time,
                    version=version
                )
        
        # Check root requirement
        if tool.requires_root and not self.is_root:
            msg = f"Tool {tool.name} requires root access"
            self.logger.warning(msg)
            return InstallResult(
                tool=tool.name,
                success=False,
                message=msg,
                duration=time.time() - start_time
            )
        
        # Install dependencies first
        for dep in tool.dependencies:
            self.logger.info(f"Checking dependency: {dep}")
            # Try to install via apt if available
            code, _, _ = self._run_cmd(["which", dep], check=False)
            if code != 0:
                self._run_cmd(["apt", "update"], timeout=120)
                self._run_cmd(["apt", "install", "-y", dep], timeout=180)
        
        # Install based on method
        success = False
        message = ""
        version = ""
        
        try:
            if tool.install_method == InstallMethod.APT:
                success, message = self._install_apt(tool)
            elif tool.install_method == InstallMethod.PIP:
                success, message = self._install_pip(tool)
            elif tool.install_method == InstallMethod.PIPX:
                success, message = self._install_pipx(tool)
            elif tool.install_method == InstallMethod.GO:
                success, message = self._install_go(tool)
            elif tool.install_method == InstallMethod.GIT:
                success, message = self._install_git(tool)
            elif tool.install_method == InstallMethod.BINARY:
                success, message = self._install_binary(tool)
            else:
                message = f"Unknown install method: {tool.install_method}"
        except Exception as e:
            message = f"Installation error: {e}"
            success = False
        
        duration = time.time() - start_time
        
        if success:
            # Verify installation
            installed, version = self._check_tool_installed(tool)
            if installed:
                self.state.installed[tool.name] = True
                if tool.name in self.state.failed:
                    del self.state.failed[tool.name]
                self.logger.info(f"✓ {tool.name} installed successfully (v{version})")
            else:
                success = False
                message = "Installation completed but verification failed"
                self.logger.warning(f"✗ {tool.name}: {message}")
        else:
            self.state.failed[tool.name] = message
            self.logger.error(f"✗ {tool.name} failed: {message}")
        
        self._save_state()
        
        return InstallResult(
            tool=tool.name,
            success=success,
            message=message,
            duration=duration,
            version=version
        )

    def install_category(self, category: ToolCategory, force: bool = False) -> List[InstallResult]:
        """Install all tools in a category."""
        category_tools = [t for t in TOOLS if t.category == category]
        results = []
        
        self.logger.info(f"Installing category: {category.value}")
        print(f"\n{'='*60}")
        print(f"Category: {category.value}")
        print(f"{'='*60}")
        
        for tool in category_tools:
            print(f"\n[*] Installing {tool.name}...")
            print(f"    {tool.description}")
            result = self.install_tool(tool, force)
            results.append(result)
            self.results.append(result)
            
            if result.success:
                print(f"    ✓ Success ({result.duration:.1f}s)")
            else:
                print(f"    ✗ Failed: {result.message}")
        
        return results

    def install_all(self, force: bool = False) -> List[InstallResult]:
        """Install all tools."""
        self.logger.info("Starting full installation of all OSINT tools")
        print(f"\n{'='*60}")
        print("FULL OSINT TOOLKIT INSTALLATION")
        print(f"{'='*60}")
        print(f"Install directory: {self.install_dir}")
        print(f"Log file: {self.log_file}")
        print(f"Termux: {self.is_termux} | Root: {self.is_root}")
        
        for category in ToolCategory:
            self.install_category(category, force)
        
        return self.results

    def generate_report(self) -> str:
        """Generate installation summary report."""
        report = []
        report.append("=" * 60)
        report.append("OSINT TOOLS INSTALLATION REPORT")
        report.append("=" * 60)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Install Directory: {self.install_dir}")
        report.append(f"Termux: {self.is_termux}")
        report.append(f"Root Access: {self.is_root}")
        report.append("")
        
        # By category
        for category in ToolCategory:
            cat_tools = [t for t in TOOLS if t.category == category]
            report.append(f"\n{category.value}")
            report.append("-" * 40)
            
            for tool in cat_tools:
                result = next((r for r in self.results if r.tool == tool.name), None)
                if result:
                    status = "✓ INSTALLED" if result.success else "✗ FAILED"
                    version = f" (v{result.version})" if result.version else ""
                    report.append(f"  {status}: {tool.name}{version}")
                    if not result.success:
                        report.append(f"    Error: {result.message}")
                elif self.state.installed.get(tool.name):
                    report.append(f"  ✓ INSTALLED: {tool.name} (from previous run)")
                elif tool.name in self.state.failed:
                    report.append(f"  ✗ FAILED: {tool.name} - {self.state.failed[tool.name]}")
                else:
                    report.append(f"  ○ PENDING: {tool.name}")
        
        # Summary
        total = len(TOOLS)
        successful = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        previously = sum(1 for t in TOOLS if self.state.installed.get(t.name) and 
                         not any(r.tool == t.name for r in self.results))
        
        report.append("\n" + "=" * 60)
        report.append("SUMMARY")
        report.append("=" * 60)
        report.append(f"Total Tools: {total}")
        report.append(f"Installed This Run: {successful}")
        report.append(f"Failed This Run: {failed}")
        report.append(f"Previously Installed: {previously}")
        report.append(f"Total Available: {successful + previously}")
        report.append("")
        report.append(f"Log file: {self.log_file}")
        report.append(f"State file: {self.state_file}")
        
        return "\n".join(report)

    def show_menu(self) -> Optional[ToolCategory]:
        """Display interactive menu and return selected category."""
        print("\n" + "=" * 60)
        print("TERMUX OSINT TOOLS INSTALLER")
        print("=" * 60)
        print("Select a category to install:")
        print()
        
        categories = list(ToolCategory)
        for i, cat in enumerate(categories, 1):
            count = len([t for t in TOOLS if t.category == cat])
            print(f"  {i}. {cat.value} ({count} tools)")
        
        print(f"  {len(categories) + 1}. Install ALL tools")
        print(f"  {len(categories) + 2}. Show installation report")
        print(f"  {len(categories) + 3}. Reset installation state")
        print("  0. Exit")
        print()
        
        while True:
            try:
                choice = input("Enter choice [0-{}]: ".format(len(categories) + 3)).strip()
                if choice == "0":
                    return None
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    return categories[idx]
                elif idx == len(categories):
                    return "ALL"
                elif idx == len(categories) + 1:
                    print(self.generate_report())
                    return "REPORT"
                elif idx == len(categories) + 2:
                    self.state = InstallState()
                    self._save_state()
                    print("Installation state reset.")
                    return "RESET"
                else:
                    print("Invalid choice. Try again.")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                return None

    def run_interactive(self):
        """Run interactive menu loop."""
        while True:
            choice = self.show_menu()
            if choice is None:
                break
            elif choice == "ALL":
                self.install_all()
                print("\n" + self.generate_report())
            elif choice == "REPORT":
                print(self.generate_report())
            elif choice == "RESET":
                continue
            else:
                self.install_category(choice)
                print("\n" + self.generate_report())
            
            input("\nPress Enter to continue...")


# ─── CLI Entry Point ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Termux OSINT Tools Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive menu
  %(prog)s --all              # Install all tools
  %(prog)s --category identity # Install identity tools only
  %(prog)s --force            # Force reinstall all tools
  %(prog)s --report           # Show installation report
  %(prog)s --reset            # Reset installation state
        """
    )
    
    parser.add_argument(
        "--all", action="store_true",
        help="Install all tools"
    )
    parser.add_argument(
        "--category", "-c", type=str,
        choices=[c.value.lower().replace(" & ", "-").replace(" ", "-") for c in ToolCategory],
        help="Install specific category"
    )
    parser.add_argument(
        "--force", "-f", action="store_true",
        help="Force reinstall even if already installed"
    )
    parser.add_argument(
        "--report", "-r", action="store_true",
        help="Show installation report"
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Reset installation state"
    )
    parser.add_argument(
        "--install-dir", type=Path, default=DEFAULT_INSTALL_DIR,
        help=f"Installation directory (default: {DEFAULT_INSTALL_DIR})"
    )
    parser.add_argument(
        "--log-dir", type=Path, default=DEFAULT_LOG_DIR,
        help=f"Log directory (default: {DEFAULT_LOG_DIR})"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {SCRIPT_VERSION}"
    )
    
    args = parser.parse_args()
    
    installer = TermuxOSINTInstaller(args.install_dir, args.log_dir)
    
    if args.reset:
        installer.state = InstallState()
        installer._save_state()
        print("Installation state reset.")
        return
    
    if args.report:
        print(installer.generate_report())
        return
    
    if args.all:
        installer.install_all(args.force)
        print("\n" + installer.generate_report())
        return
    
    if args.category:
        # Map argument to category
        cat_map = {
            "identity-people-tracking": ToolCategory.IDENTITY,
            "infrastructure-network-discovery": ToolCategory.INFRASTRUCTURE,
            "data-collection-automation": ToolCategory.COLLECTION,
            "forensics-metadata": ToolCategory.FORENSICS,
        }
        cat = cat_map.get(args.category)
        if cat:
            installer.install_category(cat, args.force)
            print("\n" + installer.generate_report())
        else:
            print(f"Unknown category: {args.category}")
        return
    
    # Interactive mode
    installer.run_interactive()


if __name__ == "__main__":
    main()