#!/usr/bin/env python3

import shutil, sys, subprocess, platform, time, os

SYSTEM = platform.system().lower()
IS_WSL = "microsoft" in platform.uname().release.lower()

if SYSTEM == "windows":
    MULTIPASS = "multipass.exe"
else:
    MULTIPASS = "multipass"

def add_env_script():
    mp_path = r"C:\Program Files\Multipass\bin"
    if os.path.exists(mp_path):
        os.environ["PATH"] += os.pathsep + mp_path
        print(f"[+] Added {mp_path} to PATH for this session.")
    else:
        print(f"[!] Multipass path not found at {mp_path}")

def run(cmd, capture_output=False, check=True, shell=True):
    print(f"\033[1;34m[+] Running:\033[0m {cmd}")
    return subprocess.run(
        cmd, shell=shell, text=True,
        capture_output=capture_output, check=check
    )

def check_multipass():
    """Verify multipass binary exists, else try to install."""
    if shutil.which(MULTIPASS) is None:
        print(f"\033[1;31m[!] {MULTIPASS} not found in PATH.\033[0m")

        if SYSTEM == "windows":
            print("\033[1;33m[>] Attempting automatic Multipass install on Windows...\033[0m")
            try:
                run("winget install --id Canonical.Multipass -e --accept-source-agreements --accept-package-agreements")
                print("\n\033[1;32m[✓] Multipass installed successfully via winget.\033[0m")
                add_env_script()
            except Exception:
                try:
                    print("\033[1;33m[>] winget not available. Falling back to MSI installer...\033[0m")
                    installer_url = "https://multipass.run/download/windows/latest"
                    installer_path = os.path.join(os.environ["TEMP"], "multipass-latest.msi")

                    ps_download = f'powershell -Command "Invoke-WebRequest -Uri {installer_url} -OutFile {installer_path}"'
                    run(ps_download)

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

def get_existing_vms():
    """Return a list of existing Multipass instance names."""
    result = subprocess.run(
        ["multipass", "list", "--format", "csv"],
        capture_output=True,
        text=True,
        check=True
    )
    lines = result.stdout.strip().splitlines()[1:]
    return [line.split(",")[0] for line in lines]

def wait_for_enter(message="Press ENTER to continue..."):
    input(f"\033[1;33m{message}\033[0m")

def main():
    print("\n\033[1;31mDisclaimer: Deactivate any SECURED network before proceeding...\033[0m")
    wait_for_enter("Press ENTER to continue...")

    check_multipass()

    existing_vms = get_existing_vms()

    while True:
        vmname = input("\n\033[1;31mPlease type a unique name for your VM instance:\033[0m ").strip()
        if vmname in existing_vms:
            print(f"\033[1;33m[!] The name '{vmname}' already exists. Please choose another.\033[0m")
        else:
            break

    print("\n\033[1;33mWould you like to use default configuration? (1 CPU, 1G RAM, 5G Disk)\033[0m")
    choice = input("Type 'y' to use defaults, or 'n' to customize: ").strip().lower()

    if choice == "n":
        print("\n\033[1;33mPlease use digits only :\033[0m")
        cpus = input("Enter number of CPUs: ")
        memory = input("Enter memory : ")
        disk = input("Enter disk size : ")

        launch_cmd = f"{MULTIPASS} launch --name {vmname} --cpus {cpus} --memory {memory}G --disk {disk}G"
    elif choice == "y":
        launch_cmd = f"{MULTIPASS} launch --name {vmname}"
    else:   
        print("\033[1;31m[!] Invalid choice. Exiting.\033[0m")
        sys.exit(1)

    run(launch_cmd)
    run(f"{MULTIPASS} exec {vmname} -- lsb_release -a")
    run(f"{MULTIPASS} list")
    run(f"{MULTIPASS} help")
    wait_for_enter()

    run(f"{MULTIPASS} start {vmname}")

    print("\n\033[1;33mNow start a shell session or use the help commands above... Let's go!\033[0m")


if __name__ == "__main__":
    main()
