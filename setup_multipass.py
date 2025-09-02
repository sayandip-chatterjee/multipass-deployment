#!/usr/bin/env python3

import shutil, sys, subprocess, platform, time, os

SYSTEM = platform.system().lower()
IS_WSL = "microsoft" in platform.uname().release.lower()

if SYSTEM == "windows":
    MULTIPASS = "multipass.exe"
else:
    MULTIPASS = "multipass"

def check_ports():
    critical_ports = [1514, 1515]

    for port in critical_ports:
        result = subprocess.run(
            f"sudo lsof -ti :{port}",
            shell=True,
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip()
        if pids:
            print(f"❌ Port {port} is already in use by PID(s): {pids}")
            print("Please free this port before running the installer.")
            result = subprocess.run(f"ps aux | grep {pids} | head -n 1", shell=True, capture_output=True, text=True)
            print()
            print(f"Process using the port :")
            print(f"{result.stdout.strip()}")
            print()
            print(f"Check 'ps aux | grep <pname>' and find out the service name associated with the PID.")
            print(f"Do a gracefull shutdown 'sudo systemctl stop <sname>' .")
            print(f"CAUTION!!! You can also use command 'sudo kill -9 {pids}' to free the port, then re-trigger the installation .")
            sys.exit(1)

    print("✅ All required ports are free. Continuing installation...")

def add_env_script():
    mp_path = r"C:\Program Files\Multipass\bin"
    if os.path.exists(mp_path):
        os.environ["PATH"] += os.pathsep + mp_path
        print(f"[+] Added {mp_path} to PATH for this session.")
    else:
        print(f"[!] Multipass path not found at {mp_path}")

def run(cmd, check=True, shell=True):
    print(f"\033[1;34m[+] Running:\033[0m {cmd}")
    return subprocess.run(cmd, shell=shell, text=True, check=check)

def check_multipass():
    """Verify multipass binary exists, else try to install."""
    if shutil.which(MULTIPASS) is None:
        print(f"\033[1;31m[!] {MULTIPASS} not found in PATH.\033[0m")

        if SYSTEM == "windows":
            print("\033[1;33m[>] Attempting automatic Multipass install on Windows...\033[0m")
            try:
                # Try winget first
                run("winget install --id Canonical.Multipass -e --accept-source-agreements --accept-package-agreements")
                print("\n\033[1;32m[✓] Multipass installed successfully via winget.\033[0m")
                add_env_script()
            except Exception:
                try:
                    print("\033[1;33m[>] winget not available. Falling back to MSI installer...\033[0m")
                    installer_url = "https://multipass.run/download/windows/latest"
                    installer_path = os.path.join(os.environ["TEMP"], "multipass-latest.msi")

                    # Download MSI using PowerShell
                    ps_download = f'powershell -Command "Invoke-WebRequest -Uri {installer_url} -OutFile {installer_path}"'
                    run(ps_download)

                    # Install MSI silently
                    run(f'msiexec /i "{installer_path}" /qn /norestart')
                    print("\n\033[1;32m[✓] Multipass installed successfully via MSI.\033[0m")
                    add_env_script()
                except Exception:
                    print("\033[1;31m[!] Automatic install failed. Please install manually:\033[0m")
                    print("➡ https://multipass.run/download/windows")
                    sys.exit(1)

        elif SYSTEM == "linux" and not IS_WSL:
            print("\033[1;33m[>] Installing Multipass via snap...\033[0m")
            try:
                run("sudo snap install multipass")
                run("sudo snap refresh")
                run("sudo chmod a+w /var/snap/multipass/common/multipass_socket", check=False)
                print("\n\033[1;32m[✓] Multipass installed successfully.\033[0m")
            except Exception:
                print("\033[1;31m[!] Failed to install multipass automatically.\033[0m")
                print("➡ Please install manually: https://multipass.run")
                sys.exit(1)

        elif IS_WSL:
            print("\033[1;31m[!] WSL detected. Multipass usually does not work in nested virtualization.\033[0m")
            print("➡ Please run the script on native Linux or Windows instead.")
            sys.exit(1)
    else:
        print(f"\033[1;32m[✓] Found {MULTIPASS} in PATH.\033[0m")

def progress_bar(duration, prefix="Progress", length=30):
    """
    Displays a progress bar in the terminal.
    
    :param duration: total time in seconds for the progress bar
    :param prefix: text before the progress bar
    :param length: length of the bar in characters
    """
    for i in range(length + 1):
        percent = i / length
        bar = "#" * i + "-" * (length - i)
        sys.stdout.write(f"\r{prefix}: [{bar}] {percent*100:.0f}%")
        sys.stdout.flush()
        time.sleep(duration / length)
    print()

def wait_for_enter(message="Press ENTER to continue..."):
    input(f"\033[1;33m{message}\033[0m")

def run(cmd, capture_output=False, check=True, shell=True):
    print(f"\033[1;34m[+] Running:\033[0m {cmd}")
    return subprocess.run(
        cmd, shell=shell, text=True,
        capture_output=capture_output, check=check
    )

def main():
    print("\n\033[1;31mDisclaimer: Deactivate any SECURED network before proceeding...\033[0m")
    wait_for_enter("Press ENTER to continue...")

    check_multipass()
    check_ports()

    vmname = input("\n\033[1;31mPlease type a unique name for your VM instance:\033[0m ")

    run(f"{MULTIPASS} launch --name {vmname} --cpus 2 --memory 4G --disk 20G")
    run(f"{MULTIPASS} exec {vmname} -- lsb_release -a")
    run(f"{MULTIPASS} list")
    run(f"{MULTIPASS} help")
    wait_for_enter()

    run(f"{MULTIPASS} start {vmname}")

    print("\n\033[1;33mNow starting a shell session with your VM... Let's go!\033[0m")
    wait_for_enter()

    os.system(f"{MULTIPASS} shell {vmname}")


if __name__ == "__main__":
    main()
