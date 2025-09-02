# 🚀 Multipass VM Setup Script

This script automates the installation and configuration of
[Multipass](https://multipass.run) and makes it easier to launch Ubuntu
VMs with customizable resources and networking.

------------------------------------------------------------------------

## 🔍 Features

-   ✅ Automatically installs **Multipass** if not found
    (Windows/Linux).
-   ✅ Interactive prompts for **CPU, memory, disk** configuration.
-   ✅ Option to use **default NAT** or **bridged networking** or customised network configuration.
-   ✅ Simple progress messages and interactive flow.

------------------------------------------------------------------------

## ⚙️ Prerequisites

- OS : Ubuntu (tested on **22.04+**) _or_ Windows (tested on **Windows11**)
- Interpreter/Runtime : **Python 3.8+** (MUST be installed in the system)
- Internet connection (to fetch Multipass if not installed).

------------------------------------------------------------------------

## ▶️ Usage

Clone or copy this repository.

[LINUX] Clone the repository and run the setup script:
```bash
git clone https://github.com/sayandip-chatterjee/multipass-deployment.git
cd multipass-deployment/
python3 setup_multipass.py
```
    
[WINDOWS] Ensure all the steps are done as mentioed:
```bash
- In the Windows machine BIOS setup, make sure that virtualization is turned on
- Install git bash - https://git-scm.com/downloads/win and close the git bash window, do not clone yet.
- Install python3.8 from Microsoft Store
- Go to Windows Features from the Start Menu -> Search and make sure You enable the
  "HyperV", "Virtual Machine Platform", and the "Windows Hypervisor Platform" to run the VM.
- Restart the machine.
- Open powershell (NOT AS Administrator)
- git clone https://github.com/sayandip-chatterjee/multipass-deployment.git
- cd multipass-deployment/
- python3 setup_multipass.py
```

## 🌐 Networking Modes [NEEDS MORE ELABORATE INFO]

In Multipass, if you don’t specify a network (--network), the VM is attached to the default NAT network that Multipass creates.

The script allows you to choose between two networking modes:

### 1. NAT (default)

-   VM gets a private IP in a Multipass-managed NAT.\
-   Outbound internet works.\
-   Only accessible from host via `multipass shell` or
    `multipass exec`.\
-   Other devices on your LAN cannot reach it.

### 2. Bridged

-   VM is attached to a host network adapter (e.g., `eth0`, `wlp2s0`).\
-   VM gets an IP from your LAN, just like a physical machine.\
-   Accessible directly from other devices on the LAN.\
-   Requires choosing a valid adapter from `multipass networks`.

------------------------------------------------------------------------

## ⚠️ Notes

-   NAT mode is simpler and always works.\
-   Bridged mode requires a supported physical adapter.\
-   Multipass networking capabilities may vary by OS and backend.
