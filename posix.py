# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,pointless-string-statement
from pathlib import Path
import os
import subprocess
import platform

appdata_path = Path.home() / (
    ".config" if not str(Path.home()).startswith("/Users/") else ""
)

def setProxy(host, port):
    try:
        # Determine the system type
        system_type = platform.system()
        proxy = f"http://{host}:{port}"

        if system_type == "Linux":
            # Check if GNOME or KDE is used
            desktop_env = os.environ.get("XDG_CURRENT_DESKTOP")
            if desktop_env and "GNOME" in desktop_env:
                # Set proxy for GNOME desktop environment
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy", "mode", "manual"],
                    check=True,
                )
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy.http", "host", host],
                    check=True,
                )
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy.http", "port", str(port)],
                    check=True,
                )
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy.https", "host", host],
                    check=True,
                )
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy.https", "port", str(port)],
                    check=True,
                )
            elif desktop_env and "KDE" in desktop_env:
                # Set proxy for KDE desktop environment
                subprocess.run(
                    [
                        "kwriteconfig5",
                        "--file",
                        "kioslaverc",
                        "--group",
                        "Proxy Settings",
                        "--key",
                        "ProxyType",
                        "1",
                    ],
                    check=True,
                )
                subprocess.run(
                    [
                        "kwriteconfig5",
                        "--file",
                        "kioslaverc",
                        "--group",
                        "Proxy Settings",
                        "--key",
                        "httpProxy",
                        proxy,
                    ],
                    check=True,
                )
                subprocess.run(
                    [
                        "kwriteconfig5",
                        "--file",
                        "kioslaverc",
                        "--group",
                        "Proxy Settings",
                        "--key",
                        "httpsProxy",
                        proxy,
                    ],
                    check=True,
                )

        elif system_type == "Darwin":
            # Set proxy for macOS (Wi-Fi, Ethernet, Thunderbolt Bridge, USB 10/100/1000 LAN)
            network_services = [
                "Wi-Fi",
                "Ethernet",
                "Thunderbolt Bridge",
                "USB 10/100/1000 LAN",
            ]
            for service in network_services:
                subprocess.run(
                    ["networksetup", "-setwebproxy", service, host, str(port)], check=True
                )
                subprocess.run(
                    ["networksetup", "-setsecurewebproxy", service, host, str(port)],
                    check=True,
                )
    except subprocess.CalledProcessError:
        pass

def clearProxy():
    try:
        # Determine the system type
        system_type = platform.system()

        if system_type == "Linux":
            # Check if GNOME or KDE is used
            desktop_env = os.environ.get("XDG_CURRENT_DESKTOP")
            if desktop_env and "GNOME" in desktop_env:
                # Clear proxy for GNOME desktop environment
                subprocess.run(
                    ["gsettings", "set", "org.gnome.system.proxy", "mode", "none"],
                    check=True,
                )
            elif desktop_env and "KDE" in desktop_env:
                # Clear proxy for KDE desktop environment
                subprocess.run(
                    [
                        "kwriteconfig5",
                        "--file",
                        "kioslaverc",
                        "--group",
                        "Proxy Settings",
                        "--key",
                        "ProxyType",
                        "0",
                    ],
                    check=True,
                )

        elif system_type == "Darwin":
            # Clear proxy for macOS (Wi-Fi, Ethernet, Thunderbolt Bridge, USB 10/100/1000 LAN)
            network_services = [
                "Wi-Fi",
                "Ethernet",
                "Thunderbolt Bridge",
                "USB 10/100/1000 LAN",
            ]
            for service in network_services:
                subprocess.run(
                    ["networksetup", "-setwebproxystate", service, "off"], check=True
                )
                subprocess.run(
                    ["networksetup", "-setsecurewebproxystate", service, "off"], check=True
                )
    except subprocess.CalledProcessError:
        pass
